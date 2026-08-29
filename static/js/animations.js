/**
 * Number Counter & Micro-Interactions (animations.js)
 */
document.addEventListener("DOMContentLoaded", () => {
    // Check for reduced motion preference
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const animationsEnabled = localStorage.getItem("cid_animations") !== "false";

    if (prefersReducedMotion || !animationsEnabled) {
        // Immediately set final values
        document.querySelectorAll("[data-count]").forEach(el => {
            const target = el.getAttribute("data-count");
            el.textContent = target;
        });
        return;
    }

    const animateCounter = (el) => {
        const targetStr = el.getAttribute("data-count");
        if (!targetStr) return;

        const isDecimal = targetStr.includes(".");
        const target = parseFloat(targetStr.replace(/,/g, ""));
        if (isNaN(target)) return;

        const duration = 1200; // ms
        const startTime = performance.now();

        const updateCount = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Ease out cubic
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const currentVal = target * easeOut;

            if (isDecimal) {
                el.textContent = currentVal.toFixed(2);
            } else {
                el.textContent = Math.round(currentVal).toLocaleString();
            }

            if (progress < 1) {
                requestAnimationFrame(updateCount);
            } else {
                el.textContent = isDecimal ? target.toFixed(2) : Math.round(target).toLocaleString();
            }
        };

        requestAnimationFrame(updateCount);
    };

    // IntersectionObserver to animate when entering viewport
    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                obs.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll("[data-count]").forEach(el => observer.observe(el));
});
