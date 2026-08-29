/**
 * Analytics & Visualization Matrix Controller (analytics.js)
 */
document.addEventListener("DOMContentLoaded", () => {
    if (!window.Chart || !window.analyticsData) return;

    const data = window.analyticsData;

    // Common Chart.js Defaults
    Chart.defaults.color = "#94A3B8";
    Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";

    const commonTooltip = {
        backgroundColor: "#1E293B",
        titleColor: "#F8FAFC",
        bodyColor: "#CBD5E1",
        borderColor: "rgba(255, 255, 255, 0.12)",
        borderWidth: 1,
        padding: 12,
        cornerRadius: 8
    };

    const commonGrid = {
        color: "rgba(255, 255, 255, 0.05)",
        drawBorder: false
    };

    // 1. Churn Ratio Doughnut Chart
    const churnCtx = document.getElementById("churnDistChart")?.getContext("2d");
    if (churnCtx) {
        new Chart(churnCtx, {
            type: "doughnut",
            data: {
                labels: ["Retained", "Churned"],
                datasets: [{
                    data: [data.retained, data.churned],
                    backgroundColor: ["#10B981", "#EF4444"],
                    borderColor: "transparent",
                    borderWidth: 0,
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: "70%",
                plugins: {
                    legend: { position: "bottom", labels: { padding: 16 } },
                    tooltip: commonTooltip
                }
            }
        });
    }

    // 2. Contract Distribution Bar Chart
    const contractCtx = document.getElementById("contractDistChart")?.getContext("2d");
    if (contractCtx && data.contracts) {
        new Chart(contractCtx, {
            type: "bar",
            data: {
                labels: Object.keys(data.contracts),
                datasets: [{
                    label: "Subscribers",
                    data: Object.values(data.contracts),
                    backgroundColor: ["#8B5CF6", "#3B82F6", "#06B6D4"],
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: commonTooltip
                },
                scales: {
                    x: { grid: { display: false } },
                    y: { grid: commonGrid }
                }
            }
        });
    }

    // 3. Churn by Contract Grouped Bar Chart
    const churnContractCtx = document.getElementById("churnByContractChart")?.getContext("2d");
    if (churnContractCtx && data.churn_by_contract) {
        const labels = Object.keys(data.churn_by_contract);
        const retainedData = labels.map(l => data.churn_by_contract[l]["No"] || 0);
        const churnedData = labels.map(l => data.churn_by_contract[l]["Yes"] || 0);

        new Chart(churnContractCtx, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: "Retained",
                        data: retainedData,
                        backgroundColor: "#10B981",
                        borderRadius: 6
                    },
                    {
                        label: "Churned",
                        data: churnedData,
                        backgroundColor: "#EF4444",
                        borderRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: "bottom", labels: { padding: 16 } },
                    tooltip: commonTooltip
                },
                scales: {
                    x: { grid: { display: false } },
                    y: { grid: commonGrid }
                }
            }
        });
    }

    // 4. Payment Method Horizontal Bar Chart
    const paymentCtx = document.getElementById("paymentDistChart")?.getContext("2d");
    if (paymentCtx && data.payment_methods) {
        new Chart(paymentCtx, {
            type: "bar",
            data: {
                labels: Object.keys(data.payment_methods),
                datasets: [{
                    label: "Subscribers",
                    data: Object.values(data.payment_methods),
                    backgroundColor: "#06B6D4",
                    borderRadius: 6
                }]
            },
            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: commonTooltip
                },
                scales: {
                    x: { grid: commonGrid },
                    y: { grid: { display: false } }
                }
            }
        });
    }

    // 5. Internet Service Doughnut Chart
    const internetCtx = document.getElementById("internetDistChart")?.getContext("2d");
    if (internetCtx && data.internet_services) {
        new Chart(internetCtx, {
            type: "doughnut",
            data: {
                labels: Object.keys(data.internet_services),
                datasets: [{
                    data: Object.values(data.internet_services),
                    backgroundColor: ["#3B82F6", "#8B5CF6", "#64748B"],
                    borderColor: "transparent",
                    borderWidth: 0,
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: "70%",
                plugins: {
                    legend: { position: "bottom", labels: { padding: 16 } },
                    tooltip: commonTooltip
                }
            }
        });
    }

    // 6. Churn by Tenure Cohort Bar Chart
    const tenureCtx = document.getElementById("tenureCohortChart")?.getContext("2d");
    if (tenureCtx && data.churn_by_tenure) {
        const labels = Object.keys(data.churn_by_tenure);
        const retainedData = labels.map(l => data.churn_by_tenure[l]["No"] || 0);
        const churnedData = labels.map(l => data.churn_by_tenure[l]["Yes"] || 0);

        new Chart(tenureCtx, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: "Retained",
                        data: retainedData,
                        backgroundColor: "#10B981",
                        borderRadius: 6
                    },
                    {
                        label: "Churned",
                        data: churnedData,
                        backgroundColor: "#EF4444",
                        borderRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: "bottom", labels: { padding: 16 } },
                    tooltip: commonTooltip
                },
                scales: {
                    x: { grid: { display: false } },
                    y: { grid: commonGrid }
                }
            }
        });
    }
});
