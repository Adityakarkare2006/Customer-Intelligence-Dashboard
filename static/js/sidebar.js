/**
 * Sidebar Navigation Controller (sidebar.js)
 */
document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.getElementById("sidebar");
    const menuToggle = document.getElementById("menuToggle");
    const sidebarOverlay = document.getElementById("sidebarOverlay");

    if (!sidebar) return;

    // Toggle Mobile Drawer or Desktop Collapse
    if (menuToggle) {
        menuToggle.addEventListener("click", (e) => {
            e.stopPropagation();
            if (window.innerWidth <= 992) {
                sidebar.classList.toggle("show");
                if (sidebarOverlay) {
                    sidebarOverlay.classList.toggle("active");
                }
            } else {
                sidebar.classList.toggle("collapsed");
            }
        });
    }

    // Close on overlay click
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener("click", () => {
            sidebar.classList.remove("show");
            sidebarOverlay.classList.remove("active");
        });
    }

    // Auto-close drawer on window resize above 992px
    window.addEventListener("resize", () => {
        if (window.innerWidth > 992 && sidebar.classList.contains("show")) {
            sidebar.classList.remove("show");
            if (sidebarOverlay) {
                sidebarOverlay.classList.remove("active");
            }
        }
    });
});