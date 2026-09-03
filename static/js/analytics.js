/**
 * ============================================================
 * CUSTOMER INTELLIGENCE HUB
 * Analytics & Visualization Controller
 * ============================================================
 */

document.addEventListener("DOMContentLoaded", function () {

    // ---------------------------------------------------------
    // Safety checks
    // ---------------------------------------------------------
    if (typeof Chart === "undefined") {
        console.error("Chart.js is not loaded.");
        return;
    }

    if (!window.analyticsData) {
        console.error("analyticsData is not available.");
        return;
    }

    const data = window.analyticsData;

    // ---------------------------------------------------------
    // Global Chart.js configuration
    // ---------------------------------------------------------
    Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";
    Chart.defaults.font.size = 12;
    Chart.defaults.color = "#94A3B8";

    // ---------------------------------------------------------
    // Helpers
    // ---------------------------------------------------------

    function getValue(value) {
        const number = Number(value);
        return Number.isFinite(number) ? number : 0;
    }

    function getCanvas(id) {
        const canvas = document.getElementById(id);

        if (!canvas) {
            console.warn(`Canvas #${id} not found.`);
            return null;
        }

        return canvas.getContext("2d");
    }

    const tooltipConfig = {
        backgroundColor: "#0F172A",
        titleColor: "#FFFFFF",
        bodyColor: "#CBD5E1",
        borderColor: "#334155",
        borderWidth: 1,
        padding: 12,
        cornerRadius: 10,
        displayColors: true
    };

    const animationConfig = {
        duration: 1200,
        easing: "easeOutQuart"
    };

    const baseOptions = {
        responsive: true,
        maintainAspectRatio: false,
        animation: animationConfig,
        plugins: {
            tooltip: tooltipConfig,
            legend: {
                labels: {
                    usePointStyle: true,
                    pointStyle: "circle",
                    padding: 18,
                    color: "#CBD5E1",
                    font: {
                        size: 12,
                        weight: "600"
                    }
                }
            }
        }
    };

    const axisOptions = {
        x: {
            grid: {
                display: false
            },
            ticks: {
                color: "#94A3B8"
            }
        },
        y: {
            beginAtZero: true,
            grid: {
                color: "rgba(148, 163, 184, 0.10)"
            },
            ticks: {
                color: "#94A3B8"
            }
        }
    };


    // =========================================================
    // 1. CHURN RATIO DOUGHNUT
    // =========================================================

    const churnCtx = getCanvas("churnDistChart");

    if (churnCtx) {

        new Chart(churnCtx, {
            type: "doughnut",

            data: {
                labels: [
                    "Retained",
                    "Churned"
                ],

                datasets: [{
                    data: [
                        getValue(data.retained),
                        getValue(data.churned)
                    ],

                    backgroundColor: [
                        "#10B981",
                        "#EF4444"
                    ],

                    borderColor: "#111827",
                    borderWidth: 4,

                    hoverOffset: 12
                }]
            },

            options: {
                ...baseOptions,

                cutout: "68%",

                plugins: {
                    ...baseOptions.plugins,

                    legend: {
                        position: "bottom",
                        labels: {
                            usePointStyle: true,
                            pointStyle: "circle",
                            padding: 20,
                            color: "#CBD5E1"
                        }
                    },

                    tooltip: tooltipConfig
                }
            }
        });
    }


    // =========================================================
    // 2. CONTRACT DISTRIBUTION
    // =========================================================

    const contractCtx = getCanvas("contractDistChart");

    if (contractCtx && data.contracts) {

        const contractLabels = Object.keys(data.contracts);

        const contractValues = contractLabels.map(function (label) {
            return getValue(data.contracts[label]);
        });

        new Chart(contractCtx, {
            type: "bar",

            data: {
                labels: contractLabels,

                datasets: [{
                    label: "Customers",

                    data: contractValues,

                    backgroundColor: [
                        "#8B5CF6",
                        "#3B82F6",
                        "#06B6D4"
                    ],

                    borderRadius: 10,

                    borderSkipped: false,

                    barThickness: 42
                }]
            },

            options: {
                ...baseOptions,

                plugins: {
                    ...baseOptions.plugins,

                    legend: {
                        display: false
                    }
                },

                scales: axisOptions
            }
        });
    }


    // =========================================================
    // 3. CHURN BY CONTRACT
    // =========================================================

    const churnContractCtx = getCanvas("churnByContractChart");

    if (churnContractCtx && data.churn_by_contract) {

        const labels = Object.keys(data.churn_by_contract);

        const retainedValues = labels.map(function (label) {

            const item = data.churn_by_contract[label];

            return getValue(
                item.No !== undefined
                    ? item.No
                    : item.retained
            );
        });

        const churnedValues = labels.map(function (label) {

            const item = data.churn_by_contract[label];

            return getValue(
                item.Yes !== undefined
                    ? item.Yes
                    : item.churned
            );
        });

        new Chart(churnContractCtx, {

            type: "bar",

            data: {
                labels: labels,

                datasets: [

                    {
                        label: "Retained",

                        data: retainedValues,

                        backgroundColor: "#10B981",

                        borderRadius: 8,

                        borderSkipped: false,

                        barThickness: 26
                    },

                    {
                        label: "Churned",

                        data: churnedValues,

                        backgroundColor: "#EF4444",

                        borderRadius: 8,

                        borderSkipped: false,

                        barThickness: 26
                    }

                ]
            },

            options: {

                ...baseOptions,

                interaction: {
                    mode: "index",
                    intersect: false
                },

                scales: axisOptions

            }
        });
    }


    // =========================================================
    // 4. PAYMENT METHOD
    // =========================================================

    const paymentCtx = getCanvas("paymentDistChart");

    if (paymentCtx && data.payment_methods) {

        const labels = Object.keys(data.payment_methods);

        const values = labels.map(function (label) {
            return getValue(data.payment_methods[label]);
        });

        new Chart(paymentCtx, {

            type: "bar",

            data: {

                labels: labels,

                datasets: [{
                    label: "Customers",

                    data: values,

                    backgroundColor: [
                        "#06B6D4",
                        "#3B82F6",
                        "#8B5CF6",
                        "#10B981"
                    ],

                    borderRadius: 8,

                    borderSkipped: false,

                    barThickness: 28
                }]
            },

            options: {

                ...baseOptions,

                indexAxis: "y",

                plugins: {

                    ...baseOptions.plugins,

                    legend: {
                        display: false
                    }
                },

                scales: {

                    x: {
                        beginAtZero: true,

                        grid: {
                            color: "rgba(148, 163, 184, 0.10)"
                        },

                        ticks: {
                            color: "#94A3B8"
                        }
                    },

                    y: {
                        grid: {
                            display: false
                        },

                        ticks: {
                            color: "#CBD5E1",
                            font: {
                                size: 11,
                                weight: "600"
                            }
                        }
                    }
                }
            }
        });
    }


    // =========================================================
    // 5. INTERNET SERVICE DISTRIBUTION
    // =========================================================

    const internetCtx = getCanvas("internetDistChart");

    if (internetCtx && data.internet_services) {

        const labels = Object.keys(data.internet_services);

        const values = labels.map(function (label) {
            return getValue(data.internet_services[label]);
        });

        new Chart(internetCtx, {

            type: "doughnut",

            data: {

                labels: labels,

                datasets: [{

                    data: values,

                    backgroundColor: [
                        "#8B5CF6",
                        "#3B82F6",
                        "#64748B"
                    ],

                    borderColor: "#111827",

                    borderWidth: 4,

                    hoverOffset: 12
                }]
            },

            options: {

                ...baseOptions,

                cutout: "65%",

                plugins: {

                    ...baseOptions.plugins,

                    legend: {

                        position: "bottom",

                        labels: {

                            usePointStyle: true,

                            pointStyle: "circle",

                            padding: 18,

                            color: "#CBD5E1"
                        }
                    }
                }
            }
        });
    }


    // =========================================================
    // 6. CHURN BY TENURE
    // =========================================================

    const tenureCtx = getCanvas("tenureCohortChart");

    if (tenureCtx && data.churn_by_tenure) {

        const labels = Object.keys(data.churn_by_tenure);

        const retainedValues = labels.map(function (label) {

            const item = data.churn_by_tenure[label];

            return getValue(
                item.No !== undefined
                    ? item.No
                    : item.retained
            );
        });

        const churnedValues = labels.map(function (label) {

            const item = data.churn_by_tenure[label];

            return getValue(
                item.Yes !== undefined
                    ? item.Yes
                    : item.churned
            );
        });

        new Chart(tenureCtx, {

            type: "bar",

            data: {

                labels: labels,

                datasets: [

                    {
                        label: "Retained",

                        data: retainedValues,

                        backgroundColor: "#10B981",

                        borderRadius: 8,

                        borderSkipped: false,

                        barThickness: 30
                    },

                    {
                        label: "Churned",

                        data: churnedValues,

                        backgroundColor: "#EF4444",

                        borderRadius: 8,

                        borderSkipped: false,

                        barThickness: 30
                    }

                ]
            },

            options: {

                ...baseOptions,

                interaction: {
                    mode: "index",
                    intersect: false
                },

                scales: axisOptions
            }
        });
    }


    // =========================================================
    // FINISHED
    // =========================================================

    console.log("✅ Analytics charts initialized successfully.");

});