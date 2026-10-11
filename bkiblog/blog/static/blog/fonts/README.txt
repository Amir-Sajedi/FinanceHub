# Web fonts: Vazirmatn via Google Fonts (no files needed here)

The site loads Vazirmatn (variable 100-900) from Google Fonts via
`<link>` tags in `templates/base.html`. Nothing in this folder is
referenced by `site.css`.

Optional later switch to licensed Anjoman files:
  1. Copy your fontiran.com files here as `Anjoman-Variable.woff2`
     (preferred) or the three static files.
  2. Add an `@font-face` for them in layer 2 of `site.css`.
  3. Change the layer-1 token to:
     `--font-sans: "Anjoman", "Vazirmatn", Tahoma, sans-serif;`
That token change is the whole switch.
