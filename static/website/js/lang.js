/**
 * Bluedot - Language Switcher (EN / AR)
 * ======================================
 * Suffix-based URL routing: /en/, /ar/, /about/en/, /about/ar/
 * Toggles html[dir] between "ltr" and "rtl".
 * Content switching is done via static .en-content / .ar-content elements in HTML.
 * Synchronizes localStorage, session cookies (bluedot_lang, django_language), and URL path.
 */

(function () {
    'use strict';

    var STORAGE_KEY = 'bluedot_lang';
    var DEFAULT_LANG = 'en';
    var SUFFIX_REGEX = /^(.*?)\/(en|ar)\/?$/;

    /* ── Detect language from current URL pathname or DOM ── */
    function getUrlLang() {
        var pathname = window.location.pathname;
        var match = pathname.match(SUFFIX_REGEX);
        if (match && (match[2] === 'en' || match[2] === 'ar')) {
            return match[2];
        }
        var docLang = document.documentElement.getAttribute('lang');
        if (docLang === 'en' || docLang === 'ar') {
            return docLang;
        }
        try {
            var saved = localStorage.getItem(STORAGE_KEY);
            if (saved === 'en' || saved === 'ar') return saved;
        } catch (e) {}
        return DEFAULT_LANG;
    }

    /* ── Apply a language to DOM elements and cookies ── */
    function applyLang(lang) {
        var html = document.documentElement;

        /* 1. Set html attributes */
        html.setAttribute('lang', lang);
        html.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');

        /* 2. Update current label badges */
        document.querySelectorAll('.lang-current-label').forEach(function (el) {
            el.textContent = lang.toUpperCase();
        });

        /* 3. Mark active option in all dropdowns */
        document.querySelectorAll('.lang-option').forEach(function (opt) {
            opt.classList.toggle('active', opt.getAttribute('data-lang') === lang);
        });

        /* 4. Update dynamic attributes for placeholders and options */
        document.querySelectorAll('[data-en][data-ar]').forEach(function (el) {
            var text = lang === 'ar' ? el.getAttribute('data-ar') : el.getAttribute('data-en');
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                el.placeholder = text;
            } else if (el.tagName === 'OPTION') {
                el.textContent = text;
            } else {
                el.textContent = text;
            }
        });

        /* 5. Save to localStorage and Cookies */
        try { localStorage.setItem(STORAGE_KEY, lang); } catch (e) {}
        document.cookie = "bluedot_lang=" + lang + "; path=/; max-age=31536000; SameSite=Lax";
        document.cookie = "django_language=" + lang + "; path=/; max-age=31536000; SameSite=Lax";
    }

    /* ── Switch to a target language by updating the URL ── */
    function switchLanguage(targetLang) {
        var pathname = window.location.pathname;
        var newPath = '';

        var match = pathname.match(SUFFIX_REGEX);
        if (match) {
            var base = match[1] || '';
            newPath = (base ? base : '') + '/' + targetLang + '/';
        } else if (pathname === '/' || pathname === '') {
            newPath = '/' + targetLang + '/';
        } else {
            var cleanPath = pathname.replace(/\/+$/, '');
            newPath = cleanPath + '/' + targetLang + '/';
        }

        // Save preference before navigation
        try { localStorage.setItem(STORAGE_KEY, targetLang); } catch (e) {}
        document.cookie = "bluedot_lang=" + targetLang + "; path=/; max-age=31536000; SameSite=Lax";
        document.cookie = "django_language=" + targetLang + "; path=/; max-age=31536000; SameSite=Lax";

        var targetUrl = newPath + window.location.search + window.location.hash;
        window.location.href = targetUrl;
    }

    /* ── Init ── */
    function init() {
        var currentLang = getUrlLang();

        /* Wire option clicks */
        document.querySelectorAll('.lang-option').forEach(function (opt) {
            opt.addEventListener('click', function (e) {
                e.preventDefault();
                e.stopPropagation();

                var selectedLang = this.getAttribute('data-lang');
                if (selectedLang !== currentLang) {
                    switchLanguage(selectedLang);
                } else {
                    /* Close all dropdowns if clicking the already active language */
                    document.querySelectorAll('.header-lang, .nav-lang').forEach(function (d) {
                        d.classList.remove('open');
                    });
                }
            });
        });

        /* Toggle dropdown open/close on trigger click */
        document.querySelectorAll('.header-lang, .nav-lang').forEach(function (trigger) {
            trigger.addEventListener('click', function (e) {
                if (e.target.closest('.lang-option')) return;
                this.classList.toggle('open');
            });
        });

        /* Close when clicking outside */
        document.addEventListener('click', function (e) {
            if (!e.target.closest('.header-lang') && !e.target.closest('.nav-lang')) {
                document.querySelectorAll('.header-lang, .nav-lang').forEach(function (d) {
                    d.classList.remove('open');
                });
            }
        });

        /* Apply on load */
        applyLang(currentLang);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
