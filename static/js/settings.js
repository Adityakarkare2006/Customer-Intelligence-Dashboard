/**
 * System Settings & Local Preferences Controller (settings.js)
 */
document.addEventListener("DOMContentLoaded", () => {
    const darkThemeToggle = document.getElementById("darkThemeToggle");
    const highContrastToggle = document.getElementById("highContrastToggle");
    const animationsToggle = document.getElementById("animationsToggle");
    const compactModeToggle = document.getElementById("compactModeToggle");
    const notificationsToggle = document.getElementById("notificationsToggle");
    const saveSettingsBtn = document.getElementById("saveSettingsBtn");

    // Load initial settings
    if (darkThemeToggle) {
        darkThemeToggle.checked = localStorage.getItem("cid_theme") !== "light";
        darkThemeToggle.addEventListener("change", () => {
            const isLight = !darkThemeToggle.checked;
            document.body.classList.toggle("light-theme", isLight);
            localStorage.setItem("cid_theme", isLight ? "light" : "dark");
        });
    }

    if (highContrastToggle) {
        highContrastToggle.checked = localStorage.getItem("cid_contrast") === "true";
        highContrastToggle.addEventListener("change", () => {
            localStorage.setItem("cid_contrast", highContrastToggle.checked ? "true" : "false");
        });
    }

    if (animationsToggle) {
        animationsToggle.checked = localStorage.getItem("cid_animations") !== "false";
        animationsToggle.addEventListener("change", () => {
            localStorage.setItem("cid_animations", animationsToggle.checked ? "true" : "false");
        });
    }

    if (compactModeToggle) {
        compactModeToggle.checked = localStorage.getItem("cid_compact") === "true";
        compactModeToggle.addEventListener("change", () => {
            localStorage.setItem("cid_compact", compactModeToggle.checked ? "true" : "false");
        });
    }

    if (notificationsToggle) {
        notificationsToggle.checked = localStorage.getItem("cid_notifications") !== "false";
        notificationsToggle.addEventListener("change", () => {
            localStorage.setItem("cid_notifications", notificationsToggle.checked ? "true" : "false");
        });
    }

    if (saveSettingsBtn) {
        saveSettingsBtn.addEventListener("click", () => {
            const originalHTML = saveSettingsBtn.innerHTML;
            saveSettingsBtn.innerHTML = `<i class="ri-check-line"></i> <span>Preferences Saved!</span>`;
            saveSettingsBtn.style.background = "#10B981";
            setTimeout(() => {
                saveSettingsBtn.innerHTML = originalHTML;
                saveSettingsBtn.style.background = "";
            }, 1500);
        });
    }
});
