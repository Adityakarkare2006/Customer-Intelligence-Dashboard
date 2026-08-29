/**
 * Top Navbar & Dropdowns Controller (navbar.js)
 */
document.addEventListener("DOMContentLoaded", () => {
    const profileButton = document.getElementById("profileButton");
    const profileMenu = document.getElementById("profileMenu");
    const notificationButton = document.getElementById("notificationButton");
    const notificationPanel = document.getElementById("notificationPanel");
    const globalSearchInput = document.getElementById("globalSearchInput");
    const topNavbar = document.querySelector(".top-navbar");

    // Profile Dropdown Toggle
    if (profileButton && profileMenu) {
        profileButton.addEventListener("click", (e) => {
            e.stopPropagation();
            const isOpen = profileMenu.classList.contains("show");
            
            // Close other dropdowns
            if (notificationPanel) notificationPanel.classList.remove("show");

            if (isOpen) {
                profileMenu.classList.remove("show");
                profileButton.classList.remove("active");
            } else {
                profileMenu.classList.add("show");
                profileButton.classList.add("active");
            }
        });
    }

    // Notification Panel Toggle
    if (notificationButton && notificationPanel) {
        notificationButton.addEventListener("click", (e) => {
            e.stopPropagation();
            const isOpen = notificationPanel.classList.contains("show");

            // Close profile dropdown
            if (profileMenu) {
                profileMenu.classList.remove("show");
                if (profileButton) profileButton.classList.remove("active");
            }

            if (isOpen) {
                notificationPanel.classList.remove("show");
            } else {
                notificationPanel.classList.add("show");
            }
        });
    }

    // Close dropdowns on outside click
    document.addEventListener("click", (e) => {
        if (profileMenu && !profileMenu.contains(e.target) && !profileButton?.contains(e.target)) {
            profileMenu.classList.remove("show");
            if (profileButton) profileButton.classList.remove("active");
        }

        if (notificationPanel && !notificationPanel.contains(e.target) && !notificationButton?.contains(e.target)) {
            notificationPanel.classList.remove("show");
        }
    });

    // Global Search redirect
    if (globalSearchInput) {
        globalSearchInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                const query = globalSearchInput.value.trim();
                if (query) {
                    window.location.href = `/customers?search=${encodeURIComponent(query)}`;
                }
            }
        });
    }

    // Navbar shadow on scroll
    window.addEventListener("scroll", () => {
        if (window.scrollY > 20) {
            topNavbar?.classList.add("navbar-scrolled");
        } else {
            topNavbar?.classList.remove("navbar-scrolled");
        }
    });
});