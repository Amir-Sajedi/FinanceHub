// ===================================
// Internationalization & Language Switcher
// ===================================

const translations = {
    en: {
        // Navigation
        'nav.home': 'Home',
        'nav.about': 'About',
        'nav.settings': 'Settings',
        'nav.hub': 'Hub',
        'nav.logout': 'Logout',
        'nav.signup': 'Sign Up',
        
        // Welcome Banner
        'welcome.back': 'Welcome back',
        
        // Hero Section
        'hero.title': 'Welcome to Finance Hub',
        'hero.subtitle': 'Your comprehensive financial management platform for currency exchange, precious metals tracking, and secure savings management.',
        'hero.cta': 'Manage Your Funds',
        
        // Features
        'features.title': 'Our Features',
        'feature1.title': 'Real-Time Currency Exchange',
        'feature1.desc': 'Convert between multiple currencies with live exchange rates. Track your conversions and monitor market trends to make informed financial decisions.',
        'feature2.title': 'Gold & Silver Converter',
        'feature2.desc': 'Calculate the value of your precious metals holdings in real-time. Convert between grams, ounces, and currency values with up-to-date market prices.',
        'feature3.title': 'Total Saved Balance',
        'feature3.desc': 'View your complete financial overview in one place. Track all your assets, conversions, and savings with detailed analytics and historical data.',
        
        // About Section
        'about.title': 'About Us',
        'about.p1': 'Finance Hub is a modern financial management platform designed to simplify your currency exchange and precious metals tracking needs. We provide secure, reliable, and user-friendly tools to help you manage your financial assets with confidence.',
        'about.p2': 'Our platform combines cutting-edge technology with intuitive design to deliver a seamless experience for both novice and experienced investors.',
        
        // Privacy Section
        'privacy.title': 'Privacy & Security',
        'privacy.p1': 'Your financial data security is our top priority. We employ industry-standard encryption protocols to protect your information and ensure all transactions are processed through secure channels.',
        'privacy.p2': 'We never share your personal data with third parties and maintain strict compliance with international data protection regulations.',
        
        // Footer
        'footer.copyright': '© 2026 Finance Hub. All rights reserved.',
        
        // Login Page
        'login.title': 'Welcome!',
        'login.subtitle': 'Sign in to continue',
        'login.username': 'Username',
        'login.password': 'Password',
        'login.remember': 'Remember me',
        'login.forgot': 'Forgot password?',
        'login.submit': 'Sign In',
        'login.noaccount': "Don't have an account?",
        'login.create': 'Create one',
        'login.error': 'Invalid Login Credentials',
        'login.error.message': 'The username or password you entered is incorrect. Please try again.',
    },
    fa: {
        // Navigation
        'nav.home': 'خانه',
        'nav.about': 'درباره ما',
        'nav.settings': 'تنظیمات',
        'nav.hub': 'هاب',
        'nav.logout': 'خروج',
        'nav.signup': 'ثبت نام',
        
        // Welcome Banner
        'welcome.back': 'خوش آمدید',
        
        // Hero Section
        'hero.title': 'به هاب مالی خوش آمدید',
        'hero.subtitle': 'پلتفرم جامع مدیریت مالی شما برای تبدیل ارز، پیگیری فلزات گرانبها و مدیریت امن پس‌انداز.',
        'hero.cta': 'مدیریت دارایی‌های شما',
        
        // Features
        'features.title': 'ویژگی‌های ما',
        'feature1.title': 'تبدیل ارز لحظه‌ای',
        'feature1.desc': 'تبدیل بین ارزهای مختلف با نرخ‌های زنده. تبدیل‌های خود را پیگیری کنید و روندهای بازار را برای تصمیم‌گیری‌های مالی آگاهانه رصد کنید.',
        'feature2.title': 'تبدیل طلا و نقره',
        'feature2.desc': 'ارزش دارایی‌های فلزات گرانبهای خود را به صورت لحظه‌ای محاسبه کنید. بین گرم، اونس و ارزش ارزی با قیمت‌های به‌روز بازار تبدیل کنید.',
        'feature3.title': 'موجودی کل پس‌انداز',
        'feature3.desc': 'نمای کلی مالی کامل خود را در یک مکان مشاهده کنید. تمام دارایی‌ها، تبدیل‌ها و پس‌اندازهای خود را با تحلیل‌های دقیق و داده‌های تاریخی پیگیری کنید.',
        
        // About Section
        'about.title': 'درباره ما',
        'about.p1': 'هاب مالی یک پلتفرم مدیریت مالی مدرن است که برای ساده‌سازی نیازهای تبدیل ارز و پیگیری فلزات گرانبهای شما طراحی شده است. ما ابزارهای امن، قابل اعتماد و کاربرپسند را برای کمک به مدیریت دارایی‌های مالی شما با اطمینان ارائه می‌دهیم.',
        'about.p2': 'پلتفرم ما فناوری پیشرفته را با طراحی شهودی ترکیب می‌کند تا تجربه‌ای یکپارچه برای سرمایه‌گذاران تازه‌کار و با تجربه ارائه دهد.',
        
        // Privacy Section
        'privacy.title': 'حریم خصوصی و امنیت',
        'privacy.p1': 'امنیت داده‌های مالی شما اولویت اصلی ما است. ما از پروتکل‌های رمزگذاری استاندارد صنعت برای محافظت از اطلاعات شما استفاده می‌کنیم و اطمینان حاصل می‌کنیم که تمام تراکنش‌ها از طریق کانال‌های امن پردازش می‌شوند.',
        'privacy.p2': 'ما هرگز داده‌های شخصی شما را با اشخاص ثالث به اشتراک نمی‌گذاریم و انطباق دقیق با مقررات بین‌المللی حفاظت از داده‌ها را حفظ می‌کنیم.',
        
        // Footer
        'footer.copyright': '© ۲۰۲۶ هاب مالی. تمامی حقوق محفوظ است.',
        
        // Login Page
        'login.title': 'خوش آمدید!',
        'login.subtitle': 'برای ادامه وارد شوید',
        'login.username': 'نام کاربری',
        'login.password': 'رمز عبور',
        'login.remember': 'مرا به خاطر بسپار',
        'login.forgot': 'رمز عبور را فراموش کرده‌اید؟',
        'login.submit': 'ورود',
        'login.noaccount': 'حساب کاربری ندارید؟',
        'login.create': 'ایجاد حساب',
        'login.error': 'اطلاعات ورود نامعتبر',
        'login.error.message': 'نام کاربری یا رمز عبور وارد شده نادرست است. لطفاً دوباره تلاش کنید.',
    }
};

// Get current language from localStorage or default to 'en'
let currentLang = localStorage.getItem('language') || 'en';

// Initialize language on page load
document.addEventListener('DOMContentLoaded', function() {
    applyLanguage(currentLang);
    
    // Add language switcher click handler
    const langBtn = document.getElementById('langToggle');
    if (langBtn) {
        langBtn.addEventListener('click', toggleLanguage);
    }
});

// Toggle between languages
function toggleLanguage() {
    currentLang = currentLang === 'en' ? 'fa' : 'en';
    localStorage.setItem('language', currentLang);
    applyLanguage(currentLang);
}

// Apply language to the page
function applyLanguage(lang) {
    const html = document.documentElement;
    
    // Set direction and lang attribute
    if (lang === 'fa') {
        html.setAttribute('dir', 'rtl');
        html.setAttribute('lang', 'fa');
    } else {
        html.setAttribute('dir', 'ltr');
        html.setAttribute('lang', 'en');
    }
    
    // Update all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        if (translations[lang] && translations[lang][key]) {
            element.textContent = translations[lang][key];
        }
    });
    
    // Update language button text
    const langBtn = document.getElementById('langToggle');
    if (langBtn) {
        const flagSpan = langBtn.querySelector('.lang-flag');
        const textSpan = langBtn.querySelector('.lang-text');
        if (lang === 'fa') {
            if (flagSpan) flagSpan.textContent = '🇺🇸';
            if (textSpan) textSpan.textContent = 'English';
        } else {
            if (flagSpan) flagSpan.textContent = '🇮🇷';
            if (textSpan) textSpan.textContent = 'فارسی';
        }
    }
}

// Toast notification system
function showToast(type, title, message, duration = 5000) {
    const container = document.getElementById('toastContainer') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const iconSvg = getToastIcon(type);
    
    toast.innerHTML = `
        <div class="toast-icon ${type}">
            ${iconSvg}
        </div>
        <div class="toast-content">
            <div class="toast-title">${title}</div>
            <div class="toast-message">${message}</div>
        </div>
        <button class="toast-close" onclick="this.parentElement.remove()">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
        </button>
    `;
    
    container.appendChild(toast);
    
    // Auto remove after duration
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
}

function getToastIcon(type) {
    const icons = {
        error: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>',
        success: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>',
        info: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>'
    };
    return icons[type] || icons.info;
}

// Export for use in other scripts
window.i18n = {
    toggleLanguage,
    applyLanguage,
    showToast,
    getCurrentLang: () => currentLang,
    translate: (key) => translations[currentLang][key] || key
};
