/**
 * Theme Switcher Controller (theme.js)
 */
(() => {
    const savedTheme = localStorage.getItem("cid_theme") || "dark";
    if (savedTheme === "light") {
        document.body.classList.add("light-theme");
    }

    document.addEventListener("DOMContentLoaded", () => {
        const themeToggle = document.getElementById("themeToggle");
        const icon = themeToggle?.querySelector("i");

        const updateIcon = () => {
            if (!icon) return;
            if (document.body.classList.contains("light-theme")) {
                icon.className = "ri-sun-line";
                themeToggle.title = "Switch to Dark Mode";
            } else {
                icon.className = "ri-moon-line";
                themeToggle.title = "Switch to Light Mode";
            }
        };

        updateIcon();

        if (themeToggle) {
            themeToggle.addEventListener("click", () => {
                const isLight = document.body.classList.toggle("light-theme");
                localStorage.setItem("cid_theme", isLight ? "light" : "dark");
                updateIcon();

                // Dispatch custom event for Chart.js updates if needed
                window.dispatchEvent(new CustomEvent("themeChanged", { detail: { theme: isLight ? "light" : "dark" } }));
            });
        }
    });
})();
