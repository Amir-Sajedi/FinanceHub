# IRANSans Font Files

To complete the Persian localization, you need to add the IRANSans font files to this directory.

## Required Files:

1. **IRANSans-Light.woff2** and **IRANSans-Light.woff**
2. **IRANSans-Regular.woff2** and **IRANSans-Regular.woff**
3. **IRANSans-Medium.woff2** and **IRANSans-Medium.woff**
4. **IRANSans-Bold.woff2** and **IRANSans-Bold.woff**

## Where to Download:

You can download IRANSans fonts from:
- Official repository: https://github.com/rastikerdar/vazir-font (or similar Persian font repositories)
- Alternative: https://fontlibrary.org/
- Or use any Persian font repository that provides IRANSans

## Installation:

1. Download the font files in WOFF2 and WOFF formats
2. Place them in this directory (`static/fonts/`)
3. The CSS is already configured in `static/css/i18n.css`

## Alternative:

If IRANSans is not available, you can use other Persian fonts like:
- Vazir
- Samim
- Shabnam

Just update the font-family name in `static/css/i18n.css` accordingly.

## Note:

The application will still work without these fonts, but Persian text will fall back to system fonts which may not render as beautifully.
