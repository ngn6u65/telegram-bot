/* ========================================
   StarStore - JavaScript
   ======================================== */

document.addEventListener('DOMContentLoaded', () => {
    initStarsBackground();
    initNavbar();
    initMobileMenu();
    initCounters();
    initFAQ();
    initPackageButtons();
    initCustomPackage();
    initOrderForm();
    initScrollAnimations();
    initSmoothScroll();
});

/* ---------- Stars Background ---------- */
function initStarsBackground() {
    const bg = document.getElementById('starsBg');
    if (!bg) return;
    const count = 120;

    for (let i = 0; i < count; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        const size = Math.random() * 2.5 + 0.5;
        star.style.cssText = `
            width: ${size}px;
            height: ${size}px;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            --duration: ${Math.random() * 4 + 2}s;
            animation-delay: ${Math.random() * 4}s;
            opacity: ${Math.random() * 0.5 + 0.2};
        `;
        bg.appendChild(star);
    }
}

/* ---------- Navbar Scroll ---------- */
function initNavbar() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    const onScroll = () => {
        navbar.classList.toggle('scrolled', window.scrollY > 50);
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    // Active link based on scroll
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const top = section.offsetTop - 120;
            if (window.scrollY >= top) {
                current = section.getAttribute('id');
            }
        });
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    }, { passive: true });
}

/* ---------- Mobile Menu ---------- */
function initMobileMenu() {
    const btn = document.getElementById('mobileMenuBtn');
    const links = document.getElementById('navLinks');
    if (!btn || !links) return;

    btn.addEventListener('click', () => {
        btn.classList.toggle('active');
        links.classList.toggle('active');
    });

    links.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            btn.classList.remove('active');
            links.classList.remove('active');
        });
    });
}

/* ---------- Animated Counters ---------- */
function initCounters() {
    const counters = document.querySelectorAll('.stat-number[data-count]');
    if (!counters.length) return;

    const animateCounter = (el) => {
        const target = parseInt(el.dataset.count, 10);
        const duration = 2000;
        const start = performance.now();

        const step = (now) => {
            const elapsed = now - start;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            const value = Math.floor(eased * target);

            el.textContent = value.toLocaleString('en');
            if (progress < 1) requestAnimationFrame(step);
            else el.textContent = target.toLocaleString('en') + (target === 99 ? '%' : '+');
        };

        requestAnimationFrame(step);
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(c => observer.observe(c));
}

/* ---------- FAQ ---------- */
function initFAQ() {
    document.querySelectorAll('.faq-question').forEach(btn => {
        btn.addEventListener('click', () => {
            const item = btn.closest('.faq-item');
            const isActive = item.classList.contains('active');
            document.querySelectorAll('.faq-item.active').forEach(i => i.classList.remove('active'));
            if (!isActive) item.classList.add('active');
        });
    });
}

/* ---------- Package Buttons ---------- */
function initPackageButtons() {
    document.querySelectorAll('.package-btn[data-stars]').forEach(btn => {
        btn.addEventListener('click', () => {
            const stars = parseInt(btn.dataset.stars, 10);
            const price = parseFloat(btn.dataset.price);
            openOrderModal(stars, price);
        });
    });
}

/* ---------- Custom Package ---------- */
function initCustomPackage() {
    const input = document.getElementById('customStars');
    const priceEl = document.getElementById('customPriceValue');
    const btn = document.getElementById('customPackageBtn');

    if (!input || !priceEl || !btn) return;

    const pricePerStar = 0.02;

    input.addEventListener('input', () => {
        const val = parseInt(input.value, 10) || 0;
        const price = (val * pricePerStar).toFixed(2);
        priceEl.textContent = `$${price}`;
    });

    btn.addEventListener('click', () => {
        const val = parseInt(input.value, 10) || 0;
        if (val < 10) {
            input.style.borderColor = '#ef4444';
            setTimeout(() => { input.style.borderColor = ''; }, 2000);
            return;
        }
        const price = (val * pricePerStar).toFixed(2);
        openOrderModal(val, parseFloat(price));
    });
}

/* ---------- Order Modal ---------- */
function openOrderModal(stars, price) {
    const modal = document.getElementById('orderModal');
    if (!modal) return;

    const bonus = getBonus(stars);

    document.getElementById('modalStars').textContent = stars.toLocaleString('en') + ' ⭐';
    document.getElementById('modalBonus').textContent = bonus > 0 ? `+${bonus} نجمة` : 'لا يوجد';
    document.getElementById('modalTotal').textContent = `$${price.toFixed(2)}`;

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function getBonus(stars) {
    if (stars >= 2500) return 500;
    if (stars >= 1000) return 150;
    if (stars >= 500) return 50;
    return 0;
}

document.getElementById('modalClose')?.addEventListener('click', closeOrderModal);
document.getElementById('orderModal')?.addEventListener('click', (e) => {
    if (e.target === e.currentTarget) closeOrderModal();
});

function closeOrderModal() {
    const modal = document.getElementById('orderModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

/* ---------- Order Form ---------- */
function initOrderForm() {
    const form = document.getElementById('orderForm');
    if (!form) return;

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const username = document.getElementById('telegramUsername').value.trim();
        if (!username) return;

        closeOrderModal();

        // Show success
        const orderNum = 'ST-' + String(Math.floor(Math.random() * 90000) + 10000);
        document.getElementById('orderNumber').textContent = '#' + orderNum;

        const successModal = document.getElementById('successModal');
        if (successModal) {
            successModal.classList.add('active');
            document.body.style.overflow = 'hidden';
            createConfetti();
        }

        // Reset form
        form.reset();
    });
}

function closeSuccessModal() {
    const modal = document.getElementById('successModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// Expose globally
window.closeSuccessModal = closeSuccessModal;

/* ---------- Confetti ---------- */
function createConfetti() {
    const container = document.getElementById('confetti');
    if (!container) return;
    container.innerHTML = '';

    const colors = ['#f5a623', '#ffd700', '#7c3aed', '#a78bfa', '#4ade80', '#ef4444', '#3b82f6'];

    for (let i = 0; i < 50; i++) {
        const piece = document.createElement('div');
        const color = colors[Math.floor(Math.random() * colors.length)];
        piece.style.cssText = `
            position: absolute;
            width: ${Math.random() * 8 + 4}px;
            height: ${Math.random() * 8 + 4}px;
            background: ${color};
            border-radius: ${Math.random() > 0.5 ? '50%' : '2px'};
            left: ${Math.random() * 100}%;
            top: 50%;
            opacity: 0;
            animation: confetti-fall ${Math.random() * 2 + 1}s ease-out ${Math.random() * 0.5}s forwards;
        `;
        container.appendChild(piece);
    }

    // Add confetti animation
    if (!document.getElementById('confetti-style')) {
        const style = document.createElement('style');
        style.id = 'confetti-style';
        style.textContent = `
            @keyframes confetti-fall {
                0% { transform: translateY(0) rotate(0deg); opacity: 1; }
                100% { transform: translateY(-200px) translateX(${Math.random() > 0.5 ? '' : '-'}${Math.random() * 100}px) rotate(${Math.random() * 720}deg); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }
}

/* ---------- Scroll Animations ---------- */
function initScrollAnimations() {
    const elements = document.querySelectorAll('[data-aos]');
    if (!elements.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const delay = entry.target.dataset.aosDelay || 0;
                setTimeout(() => {
                    entry.target.classList.add('aos-animate');
                }, parseInt(delay, 10));
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    elements.forEach(el => observer.observe(el));
}

/* ---------- Smooth Scroll ---------- */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', (e) => {
            const id = link.getAttribute('href');
            if (id === '#') return;
            const target = document.querySelector(id);
            if (target) {
                e.preventDefault();
                const offset = 80;
                const top = target.getBoundingClientRect().top + window.scrollY - offset;
                window.scrollTo({ top, behavior: 'smooth' });
            }
        });
    });
}
