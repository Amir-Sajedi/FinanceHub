# Finance Hub - Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Verify Installation
All refactoring files are already in place. Check that these exist:
```bash
ls static/css/i18n.css
ls static/css/logo-3d.css
ls static/js/i18n.js
ls templates/base.html
```

### Step 2: (Optional) Add Persian Fonts
For optimal Persian typography, download IRANSans fonts:
```bash
# See static/fonts/README.md for download links
# Place .woff2 and .woff files in static/fonts/
```

### Step 3: Run the Server
```bash
python manage.py runserver
```

Visit: `http://localhost:8000/`

---

## 🎯 Key Features to Test

### 1. Language Switcher
- **Location:** Top-right corner of navigation bar
- **Action:** Click the button with flag emoji
- **Result:** Page switches between English (LTR) and Persian (RTL)
- **Persistence:** Language preference saved in browser

### 2. 3D Logo
- **Location:** Hero section on homepage
- **Features:** 
  - Floating animation
  - 3D perspective with tilt
  - Gradient backgrounds
  - Glow effect

### 3. Hub Button
- **Location:** Navigation bar (when logged in)
- **Features:**
  - Purple gradient background
  - Shimmer effect on hover
  - Scale and lift animation
  - Distinct from other nav items

### 4. Login Error Handling
- **Location:** Login page (`/login/`)
- **Test:** Enter wrong credentials
- **Result:** Toast notification appears with error message
- **Languages:** Error message in current language (EN/FA)

---

## 📱 Responsive Testing

### Desktop View (> 768px)
```
✓ 3-column feature grid
✓ Large 3D logo (180px)
✓ Full navigation bar
✓ Side-positioned toasts
```

### Mobile View (< 768px)
```
✓ Single-column layout
✓ Smaller logo (140px)
✓ Wrapped navigation
✓ Full-width toasts
```

---

## 🎨 Customization

### Change Colors
Edit `blog/static/blog/index.css`:
```css
:root {
    --primary-green: #14b8a6;      /* Main brand color */
    --gradient-hub: linear-gradient(...);  /* Hub button */
    --gradient-fintech: linear-gradient(...);  /* Headings */
}
```

### Add Translations
Edit `static/js/i18n.js`:
```javascript
const translations = {
    en: { 'new.key': 'English text' },
    fa: { 'new.key': 'متن فارسی' }
};
```

Then add to HTML:
```html
<span data-i18n="new.key">Default text</span>
```

### Modify 3D Logo
Edit `static/css/logo-3d.css`:
```css
.finance-hub-logo-3d {
    width: 180px;  /* Change size */
    animation: float 6s ease-in-out infinite;  /* Adjust animation */
}
```

---

## 🐛 Troubleshooting

### Issue: Language switcher not working
**Solution:** Check browser console for JavaScript errors. Ensure `i18n.js` is loaded.

### Issue: 3D logo not displaying
**Solution:** Check if `logo-3d.css` is linked in the template. Verify CSS 3D transform support.

### Issue: Persian text looks wrong
**Solution:** Install IRANSans fonts in `static/fonts/`. See `static/fonts/README.md`.

### Issue: RTL layout broken
**Solution:** Ensure `i18n.css` is loaded. Check `html[dir="rtl"]` styles in browser inspector.

---

## 📚 Documentation

- **Full Guide:** `REFACTORING_GUIDE.md`
- **Summary:** `IMPLEMENTATION_SUMMARY.md`
- **Structure:** `PROJECT_STRUCTURE.txt`
- **This File:** `QUICK_START.md`

---

## ✅ Verification Checklist

Before deploying to production:

- [ ] Test language switcher on all pages
- [ ] Verify RTL layout with Persian content
- [ ] Check 3D logo animation performance
- [ ] Test login error notifications
- [ ] Verify responsive design on mobile
- [ ] Check all translations are accurate
- [ ] Test with different browsers
- [ ] Verify font loading (or fallbacks)
- [ ] Check accessibility (keyboard navigation)
- [ ] Test with slow network connection

---

## 🎉 You're Ready!

The Finance Hub application is now:
- ✅ Fully bilingual (Persian/English)
- ✅ Modern and professional design
- ✅ Enhanced user experience
- ✅ Production-ready

**Happy coding!** 🚀
