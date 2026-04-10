const navbar = document.getElementById("navbar");
const menuToggle = document.getElementById("menu-toggle");
const navLinks = document.getElementById("nav-links");
const yearEl = document.getElementById("current-year");

function setCurrentYear() {
    if (yearEl) {
        yearEl.textContent = String(new Date().getFullYear());
    }
}

function handleNavbarScroll() {
    if (!navbar) {
        return;
    }

    if (window.scrollY > 24) {
        navbar.classList.add("scrolled");
    } else {
        navbar.classList.remove("scrolled");
    }
}

function setupMobileMenu() {
    if (!menuToggle || !navLinks) {
        return;
    }

    menuToggle.addEventListener("click", () => {
        const willOpen = !navLinks.classList.contains("open");
        navLinks.classList.toggle("open");
        menuToggle.setAttribute("aria-expanded", String(willOpen));
    });

    navLinks.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => {
            navLinks.classList.remove("open");
            menuToggle.setAttribute("aria-expanded", "false");
        });
    });
}

function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener("click", (event) => {
            const href = anchor.getAttribute("href");
            if (!href || href.length < 2) {
                return;
            }

            const target = document.querySelector(href);
            if (!target) {
                return;
            }

            event.preventDefault();
            target.scrollIntoView({ behavior: "smooth", block: "start" });
        });
    });
}

function setupRevealAnimation() {
    const revealEls = document.querySelectorAll(".reveal");
    if (revealEls.length === 0) {
        return;
    }

    const observer = new IntersectionObserver(
        (entries, obs) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("in");
                    obs.unobserve(entry.target);
                }
            });
        },
        {
            rootMargin: "0px 0px -80px 0px",
            threshold: 0.12,
        },
    );

    revealEls.forEach((el) => observer.observe(el));
}

function setupDocumentToggles() {
    const toggles = document.querySelectorAll(".toggle-doc");

    toggles.forEach((button) => {
        button.addEventListener("click", () => {
            const targetId = button.getAttribute("data-target");
            if (!targetId) {
                return;
            }

            const target = document.getElementById(targetId);
            if (!target) {
                return;
            }

            const isOpening = target.hasAttribute("hidden");

            toggles.forEach((otherButton) => {
                const otherTargetId = otherButton.getAttribute("data-target");
                if (!otherTargetId) {
                    return;
                }

                const otherTarget = document.getElementById(otherTargetId);
                if (!otherTarget) {
                    return;
                }

                otherTarget.setAttribute("hidden", "hidden");
                otherButton.textContent = "Ler no site";
                otherButton.setAttribute("aria-expanded", "false");
            });

            if (isOpening) {
                target.removeAttribute("hidden");
                button.textContent = "Fechar";
                button.setAttribute("aria-expanded", "true");
            }
        });
    });
}

window.addEventListener("scroll", handleNavbarScroll);
window.addEventListener("DOMContentLoaded", () => {
    setCurrentYear();
    handleNavbarScroll();
    setupMobileMenu();
    setupSmoothScroll();
    setupRevealAnimation();
    setupDocumentToggles();
});