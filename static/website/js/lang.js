/**
 * Bluedot - Language Switcher (EN / AR)
 * ======================================
 * Toggles html[dir] between "ltr" and "rtl".
 * Content switching is done via static .en-content / .ar-content elements in HTML.
 * No dynamic text replacement — no flash, no broken tags.
 */

(function () {
    'use strict';

    var STORAGE_KEY = 'bluedot_lang';
    var DEFAULT_LANG = 'en';

    /* ── Apply a language ── */
    function applyLang(lang) {
        var html = document.documentElement;

        /* 1. Set html attributes */
        html.setAttribute('lang', lang);
        html.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');

        /* 2. Update current label badges */
        document.querySelectorAll('.lang-current-label').forEach(function (el) {
            el.textContent = lang.toUpperCase();
        });

        /* 3. Mark active option */
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

        /* 5. Save */
        try { localStorage.setItem(STORAGE_KEY, lang); } catch (e) {}
    }

    /* ── Init ── */
    function init() {
        /* Read saved preference */
        var saved;
        try { saved = localStorage.getItem(STORAGE_KEY); } catch (e) {}
        var lang = saved || DEFAULT_LANG;

        /* Wire option clicks */
        document.querySelectorAll('.lang-option').forEach(function (opt) {
            opt.addEventListener('click', function (e) {
                e.preventDefault();
                e.stopPropagation();
                
                var selectedLang = this.getAttribute('data-lang');
                var currentLang = document.documentElement.getAttribute('lang') || DEFAULT_LANG;
                console.log("Language option clicked:", selectedLang, "Current lang:", currentLang);

                if (selectedLang !== currentLang) {
                    try { 
                        localStorage.setItem(STORAGE_KEY, selectedLang);
                        console.log("Set STORAGE_KEY in localStorage to:", selectedLang);
                    } catch (err) {
                        console.error("Error setting localStorage:", err);
                    }
                    // Reload the page to allow Swiper and other plugins to re-initialize with the correct RTL/LTR layout
                    window.location.reload();
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
        applyLang(lang);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
