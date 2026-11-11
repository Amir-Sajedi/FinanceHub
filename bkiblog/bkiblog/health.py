from django.http import JsonResponse


def healthz(request):
    """Lightweight liveness probe for Docker and Render health checks."""
    return JsonResponse({'status': 'ok'})
