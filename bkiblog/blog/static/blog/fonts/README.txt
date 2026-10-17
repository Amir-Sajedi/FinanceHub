# Vazirmatn webfont (self-hosted)

The site self-hosts Vazirmatn's variable web font. No Google Fonts dependency.

File in use:
  Vazirmatn-Variable.woff2
  = Vazirmatn v33.003 variable font, weight axis 100-900.
  Source: https://cdn.jsdelivr.net/npm/vazirmatn@33.0.3/fonts/webfonts/Vazirmatn%5Bwght%5D.woff2

Wiring:
  1. @font-face lives in layer 2 of ../../site.css (font-weight: 100 900, font-display: swap).
  2. templates/base.html preloads this exact file and the token is
     --font-sans: "Vazirmatn", Tahoma, sans-serif.
  3. To update: replace this file (same name), bump ?v= on site.css in base.html,
     then run `python manage.py collectstatic` on the server.

بک‌نوت: قلم وزیرمتن از همین پوشه بارگذاری می‌شود؛ وابستگی به Google Fonts حذف شده است.
