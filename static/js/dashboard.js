/**
 * Executive Dashboard Analytics & Charts Controller (dashboard.js)
 */
document.addEventListener("DOMContentLoaded", () => {
    const chartCanvas = document.getElementById("churnChart");
    if (!chartCanvas || !window.Chart) return;

    const data = window.dashboardData || {
        churnedCustomers: 1869,
        retainedCustomers: 5174,
        totalCustomers: 7043
    };

    const ctx = chartCanvas.getContext("2d");

    // Doughnut Chart Configuration
    const churnChart = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["Retained Customers", "Churned Customers"],
            datasets: [{
                data: [data.retainedCustomers, data.churnedCustomers],
                backgroundColor: [
                    "#10B981", // Green
                    "#EF4444"  // Red
                ],
                borderColor: [
                    "rgba(16, 185, 129, 0.4)",
                    "rgba(239, 68, 68, 0.4)"
                ],
                borderWidth: 2,
                hoverOffset: 6,
                spacing: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: "74%",
            plugins: {
                legend: {
                    display: false // Using custom styled HTML legend
                },
                tooltip: {
                    backgroundColor: "#1E293B",
                    titleColor: "#F8FAFC",
                    bodyColor: "#94A3B8",
                    borderColor: "rgba(255, 255, 255, 0.1)",
                    borderWidth: 1,
                    padding: 12,
                    boxPadding: 6,
                    usePointStyle: true,
                    callbacks: {
                        label: function(context) {
                            const val = context.parsed || 0;
                            const total = data.retainedCustomers + data.churnedCustomers;
                            const pct = total > 0 ? ((val / total) * 100).toFixed(1) : 0;
                            return ` ${context.label}: ${val.toLocaleString()} (${pct}%)`;
                        }
                    }
                }
            },
            animation: {
                animateScale: true,
                animateRotate: true,
                duration: 1000
            }
        }
    });

    // Update on theme change
    window.addEventListener("themeChanged", () => {
        churnChart.update();
    });
});