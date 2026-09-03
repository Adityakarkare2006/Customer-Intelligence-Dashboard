/* =========================================================
   CUSTOMER INTELLIGENCE DASHBOARD
   DASHBOARD CHARTS
========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    const data = window.dashboardData || {};

    const churned =
        Number(data.churnedCustomers || 0);

    const retained =
        Number(data.retainedCustomers || 0);

    const total =
        Number(data.totalCustomers || 0);

    /* =====================================================
       CHURN DOUGHNUT
    ===================================================== */

    const churnCanvas =
        document.getElementById("churnChart");

    if (churnCanvas) {

        new Chart(
            churnCanvas,
            {

                type: "doughnut",

                data: {

                    labels: [
                        "Churned Customers",
                        "Retained Customers"
                    ],

                    datasets: [

                        {

                            data: [
                                churned,
                                retained
                            ],

                            backgroundColor: [
                                "#ef4444",
                                "#10b981"
                            ],

                            borderColor: "#0b1220",

                            borderWidth: 4,

                            hoverOffset: 8

                        }

                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    cutout: "68%",

                    plugins: {

                        legend: {

                            position: "bottom",

                            labels: {

                                color: "#aeb8c8",

                                padding: 16,

                                font: {
                                    size: 11
                                }

                            }

                        },

                        tooltip: {

                            callbacks: {

                                label: function (context) {

                                    const value =
                                        context.raw;

                                    const percentage =
                                        total > 0
                                            ? (
                                                value /
                                                total *
                                                100
                                            ).toFixed(1)
                                            : 0;

                                    return (
                                        context.label +
                                        ": " +
                                        value.toLocaleString() +
                                        " (" +
                                        percentage +
                                        "%)"
                                    );

                                }

                            }

                        }

                    }

                }

            }
        );

    }


    /* =====================================================
       OVERVIEW BAR CHART
    ===================================================== */

    const overviewCanvas =
        document.getElementById(
            "overviewChart"
        );

    if (overviewCanvas) {

        new Chart(
            overviewCanvas,
            {

                type: "bar",

                data: {

                    labels: [
                        "Total",
                        "Churned",
                        "Retained"
                    ],

                    datasets: [

                        {

                            label:
                                "Customers",

                            data: [
                                total,
                                churned,
                                retained
                            ],

                            backgroundColor: [
                                "#7c3aed",
                                "#ef4444",
                                "#10b981"
                            ],

                            borderRadius: 7,

                            maxBarThickness: 55

                        }

                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    plugins: {

                        legend: {
                            display: false
                        }

                    },

                    scales: {

                        x: {

                            ticks: {
                                color: "#7f8ba0"
                            },

                            grid: {
                                display: false
                            }

                        },

                        y: {

                            beginAtZero: true,

                            ticks: {
                                color: "#7f8ba0"
                            },

                            grid: {
                                color:
                                    "rgba(255,255,255,0.05)"
                            }

                        }

                    }

                }

            }
        );

    }

});