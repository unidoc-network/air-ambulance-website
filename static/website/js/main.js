/**
 * Bluedot - Main JavaScript
 * ========================
 */

document.addEventListener('DOMContentLoaded', () => {

    // ============================
    // Header Scroll Effect
    // ============================
    const header = document.getElementById('siteHeader');

    const handleHeaderScroll = () => {
        const logoImg = header.querySelector('.header-logo img');
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
            if (header.classList.contains('site-header-light') && logoImg) {
                logoImg.src = '/static/website/images/main-logo.png';
            }
        } else {
            header.classList.remove('scrolled');
            if (header.classList.contains('site-header-light') && logoImg) {
                logoImg.src = '/static/website/images/bl-logo.png';
            }
        }
    };

    window.addEventListener('scroll', handleHeaderScroll);
    handleHeaderScroll(); // Run on load

    // ============================
    // Hamburger Menu Toggle
    // ============================
    const hamburger = document.getElementById('headerHamburger');
    const headerNav = document.getElementById('headerNav');
    const headerNavOverlay = document.getElementById('headerNavOverlay');
    const navCloseBtn = document.getElementById('navCloseBtn');

    if (hamburger && headerNav) {
        const toggleMenu = (forceClose = false) => {
            const isCurrentlyOpen = headerNav.classList.contains('open');
            const shouldOpen = forceClose ? false : !isCurrentlyOpen;

            if (shouldOpen) {
                hamburger.classList.add('active');
                headerNav.classList.add('open');
                if (headerNavOverlay) headerNavOverlay.classList.add('open');
                document.body.style.overflow = 'hidden';
            } else {
                hamburger.classList.remove('active');
                headerNav.classList.remove('open');
                if (headerNavOverlay) headerNavOverlay.classList.remove('open');
                document.body.style.overflow = '';

                // Reset submenu when closing the main menu component
                const navMenusWrapper = document.getElementById('navMenusWrapper');
                if (navMenusWrapper) {
                    setTimeout(() => navMenusWrapper.classList.remove('show-submenu'), 400); // 400ms delay to smoothly reset behind closed drawer
                }
            }
        };

        hamburger.addEventListener('click', () => toggleMenu());
        if (navCloseBtn) navCloseBtn.addEventListener('click', () => toggleMenu(true));
        if (headerNavOverlay) headerNavOverlay.addEventListener('click', () => toggleMenu(true));

        // Close nav when link is clicked, but not submenus
        document.querySelectorAll('.header-nav-links a:not(.has-submenu)').forEach(link => {
            link.addEventListener('click', () => toggleMenu(true));
        });

        // ============================
        // Nav Drawer Submenu Sliding
        // ============================
        const navMenusWrapper = document.getElementById('navMenusWrapper');
        const submenuLinks = document.querySelectorAll('.has-submenu');
        const navBackBtn = document.getElementById('navBackBtn');

        if (submenuLinks.length > 0 && navMenusWrapper) {
            submenuLinks.forEach(link => {
                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    navMenusWrapper.classList.add('show-submenu');
                });
            });

            if (navBackBtn) {
                navBackBtn.addEventListener('click', () => {
                    navMenusWrapper.classList.remove('show-submenu');
                });
            }
        }
    }

    // ============================
    // Enquiry Drawer Toggle
    // ============================
    const enquiryTriggers = document.querySelectorAll('.trigger-enquiry');
    const enquiryDrawer = document.getElementById('enquiryDrawer');
    const enquiryOverlay = document.getElementById('enquiryDrawerOverlay');
    const enquiryClose = document.getElementById('enquiryCloseBtn');

    if (enquiryDrawer) {
        const toggleEnquiry = (show = true) => {
            if (show) {
                enquiryDrawer.classList.add('open');
                if (enquiryOverlay) enquiryOverlay.classList.add('open');
                document.body.style.overflow = 'hidden';

                // Close the main nav if it's open
                const navDrawer = document.getElementById('headerNav');
                const hamburgerIcon = document.getElementById('headerHamburger');
                const navOverlay = document.getElementById('headerNavOverlay');

                if (navDrawer && navDrawer.classList.contains('open')) {
                    navDrawer.classList.remove('open');
                    if (hamburgerIcon) hamburgerIcon.classList.remove('active');
                    if (navOverlay) navOverlay.classList.remove('open');
                }
            } else {
                enquiryDrawer.classList.remove('open');
                if (enquiryOverlay) enquiryOverlay.classList.remove('open');
                document.body.style.overflow = '';
            }
        };

        enquiryTriggers.forEach(trigger => {
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                toggleEnquiry(true);
            });
        });

        if (enquiryClose) enquiryClose.addEventListener('click', () => toggleEnquiry(false));
        if (enquiryOverlay) enquiryOverlay.addEventListener('click', () => toggleEnquiry(false));
    }


    // ============================
    // Active Nav Link Highlighter
    // ============================
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.header-nav-links a');

    const highlightActiveLink = () => {
        const scrollPos = window.scrollY + 120;

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');

            if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    };

    window.addEventListener('scroll', highlightActiveLink);

    // ============================
    // Back to Top Button
    // ============================
    const backToTopBtn = document.getElementById('backToTop');

    if (backToTopBtn) {
        const toggleBackToTop = () => {
            if (window.scrollY > 400) {
                backToTopBtn.classList.add('visible');
            } else {
                backToTopBtn.classList.remove('visible');
            }
        };

        window.addEventListener('scroll', toggleBackToTop);

        backToTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // ============================
    // Scroll Reveal Animation
    // ============================
    const fadeInElements = document.querySelectorAll('.fade-in-up');

    const revealOnScroll = () => {
        fadeInElements.forEach(el => {
            const elTop = el.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;

            if (elTop < windowHeight - 80) {
                el.classList.add('visible');
            }
        });
    };

    window.addEventListener('scroll', revealOnScroll);
    revealOnScroll(); // Run on load

    // ============================
    // Smooth Scroll for Anchor Links
    // ============================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetEl = document.querySelector(targetId);
            if (targetEl) {
                e.preventDefault();
                targetEl.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // ============================
    // Typing / Counter Animation
    // ============================
    const counters = document.querySelectorAll('.stat-number');
    let countersAnimated = false;

    const animateCounters = () => {
        if (countersAnimated) return;

        counters.forEach(counter => {
            const rect = counter.getBoundingClientRect();
            if (rect.top < window.innerHeight) {
                countersAnimated = true;
                const target = parseInt(counter.getAttribute('data-count'), 10);
                if (isNaN(target)) return;

                let current = 0;
                const step = Math.ceil(target / 60);
                const duration = 1500;
                const increment = target / (duration / 16);

                const updateCounter = () => {
                    current += increment;
                    if (current >= target) {
                        counter.textContent = target + '+';
                    } else {
                        counter.textContent = Math.floor(current) + '+';
                        requestAnimationFrame(updateCounter);
                    }
                };

                requestAnimationFrame(updateCounter);
            }
        });
    };

    window.addEventListener('scroll', animateCounters);
    animateCounters(); // Run on load

    // ============================
    // Current Year in Footer
    // ============================
    const yearEl = document.querySelector('.current-year');
    if (yearEl) {
        yearEl.textContent = new Date().getFullYear();
    }

    console.log('🔵 Bluedot website loaded successfully!');
});
