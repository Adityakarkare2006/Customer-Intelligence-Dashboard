document.addEventListener("DOMContentLoaded", function () {

    const STORAGE_KEY = "customerIntelligenceSettings";

    const defaultSettings = {
        darkTheme: true,
        highContrast: false,
        animations: true,
        compactMode: false,
        reducedMotion: false,
        notifications: true,
        predictionAlerts: true,
        riskScore: true,
        aiRecommendations: true
    };


    const elements = {
        darkTheme: document.getElementById("darkThemeToggle"),
        highContrast: document.getElementById("highContrastToggle"),
        animations: document.getElementById("animationsToggle"),
        compactMode: document.getElementById("compactModeToggle"),
        reducedMotion: document.getElementById("reducedMotionToggle"),
        notifications: document.getElementById("notificationsToggle"),
        predictionAlerts: document.getElementById("predictionAlertsToggle"),
        riskScore: document.getElementById("riskScoreToggle"),
        aiRecommendations: document.getElementById("aiRecommendationsToggle")
    };


    function loadSettings() {

        let saved = {};

        try {
            saved = JSON.parse(
                localStorage.getItem(STORAGE_KEY) || "{}"
            );
        } catch (error) {
            saved = {};
        }

        const settings = {
            ...defaultSettings,
            ...saved
        };

        Object.keys(elements).forEach(function (key) {

            if (elements[key]) {
                elements[key].checked = Boolean(settings[key]);
            }

        });

        applySettings(settings);
    }


    function getCurrentSettings() {

        return {
            darkTheme: elements.darkTheme?.checked ?? true,
            highContrast: elements.highContrast?.checked ?? false,
            animations: elements.animations?.checked ?? true,
            compactMode: elements.compactMode?.checked ?? false,
            reducedMotion: elements.reducedMotion?.checked ?? false,
            notifications: elements.notifications?.checked ?? true,
            predictionAlerts: elements.predictionAlerts?.checked ?? true,
            riskScore: elements.riskScore?.checked ?? true,
            aiRecommendations: elements.aiRecommendations?.checked ?? true
        };
    }


    function applySettings(settings) {

        document.documentElement.classList.toggle(
            "high-contrast",
            settings.highContrast
        );

        document.documentElement.classList.toggle(
            "compact-mode",
            settings.compactMode
        );

        document.documentElement.classList.toggle(
            "reduced-motion",
            settings.reducedMotion || !settings.animations
        );
    }


    function saveSettings(showMessage = true) {

        const settings = getCurrentSettings();

        localStorage.setItem(
            STORAGE_KEY,
            JSON.stringify(settings)
        );

        applySettings(settings);

        if (showMessage) {
            showSavedMessage();
        }
    }


    function showSavedMessage() {

        const status = document.getElementById(
            "settingsStatus"
        );

        const saveButtons = [
            document.getElementById("saveSettingsBtn"),
            document.getElementById("saveSettingsBottom")
        ];

        if (status) {
            status.textContent =
                "Preferences saved successfully";
        }

        saveButtons.forEach(function (button) {

            if (!button) return;

            const original = button.innerHTML;

            button.innerHTML =
                '<i class="ri-check-line"></i> Saved';

            button.classList.add("saved-state");

            setTimeout(function () {

                button.innerHTML = original;
                button.classList.remove("saved-state");

            }, 1800);

        });

        setTimeout(function () {

            if (status) {
                status.textContent =
                    "All changes are saved locally";
            }

        }, 2000);
    }


    function resetSettings() {

        const confirmed = confirm(
            "Reset all interface preferences to their default values?"
        );

        if (!confirmed) {
            return;
        }

        localStorage.removeItem(STORAGE_KEY);

        Object.keys(elements).forEach(function (key) {

            if (elements[key]) {
                elements[key].checked =
                    Boolean(defaultSettings[key]);
            }

        });

        applySettings(defaultSettings);

        const status = document.getElementById(
            "settingsStatus"
        );

        if (status) {
            status.textContent =
                "Preferences restored to defaults";
        }

        setTimeout(function () {

            if (status) {
                status.textContent =
                    "All changes are saved locally";
            }

        }, 2000);
    }


    function toggleChangeHandler() {

        const settings = getCurrentSettings();

        applySettings(settings);

        const status = document.getElementById(
            "settingsStatus"
        );

        if (status) {
            status.textContent =
                "Unsaved changes";
        }
    }


    Object.values(elements).forEach(function (element) {

        if (!element) return;

        element.addEventListener(
            "change",
            toggleChangeHandler
        );

    });


    document
        .getElementById("saveSettingsBtn")
        ?.addEventListener(
            "click",
            function () {
                saveSettings(true);
            }
        );


    document
        .getElementById("saveSettingsBottom")
        ?.addEventListener(
            "click",
            function () {
                saveSettings(true);
            }
        );


    document
        .getElementById("resetSettingsBtn")
        ?.addEventListener(
            "click",
            resetSettings
        );


    document
        .getElementById("resetPreferencesBtn")
        ?.addEventListener(
            "click",
            resetSettings
        );


    loadSettings();

});