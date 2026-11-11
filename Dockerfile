# Multi-stage build: wheels are installed in the builder and only the virtual
# environment is copied into the slim runtime, so compilers and pip caches never
# become part of the deployed image.

FROM python:3.13.12-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /build

# Dependency manifests first so source changes do not invalidate this layer.
COPY bkiblog/requirements-prod.txt ./requirements-prod.txt

# Install dependencies; pip itself is not needed by the running service.
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir --no-compile -r requirements-prod.txt \
    && /opt/venv/bin/pip uninstall -y pip


FROM python:3.13.12-slim-bookworm AS runtime

LABEL org.opencontainers.image.title="FinanceHub" \
      org.opencontainers.image.description="Django financial conversion and net-worth tracker" \
      org.opencontainers.image.source="https://github.com/Amir-Sajedi/FinanceHub" \
      org.opencontainers.image.licenses="Proprietary"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=bkiblog.settings \
    DJANGO_DEBUG=false \
    PORT=8000 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Run the application as an unprivileged user. UID/GID are explicit so mounted
# volumes, if added later, have predictable ownership.
RUN groupadd --gid 10001 app \
    && useradd --uid 10001 --gid app --home-dir /app --no-create-home --shell /usr/sbin/nologin app

COPY --from=builder /opt/venv /opt/venv
COPY --chown=app:app bkiblog/ /app/

# collectstatic needs a secret only because DEBUG is false; this value is
# throwaway and is never used by the running service.
RUN DJANGO_SECRET_KEY=collectstatic-build-only python manage.py collectstatic --noinput

USER app

EXPOSE 8000

# Uses only the Python standard library, so no curl/wget is added to the image.
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import os, urllib.request; urllib.request.urlopen('http://127.0.0.1:{}/healthz/'.format(os.environ.get('PORT', '8000')), timeout=3)"

# Render assigns PORT (default 10000); 8000 keeps local Docker runs conventional.
# exec keeps Gunicorn as PID 1 so it receives signals directly.
CMD ["sh", "-c", "exec gunicorn bkiblog.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers ${WEB_CONCURRENCY:-2} --timeout ${GUNICORN_TIMEOUT:-60} --access-logfile - --error-logfile -"]
