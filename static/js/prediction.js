/**
 * Machine Learning Prediction Controller (prediction.js)
 */
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("predictionForm");
    const highRiskBtn = document.getElementById("loadHighRiskSampleBtn");
    const lowRiskBtn = document.getElementById("loadLowRiskSampleBtn");
    const submitBtn = document.getElementById("submitPredictionBtn");
    const resultSection = document.getElementById("predictionResultSection");

    // Scroll to results if present on load
    if (resultSection) {
        resultSection.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }

    const fillForm = (values) => {
        for (const [name, val] of Object.entries(values)) {
            const input = form.querySelector(`[name="${name}"]`);
            if (input) {
                input.value = val;
                // Add highlight flash
                input.style.borderColor = "var(--accent)";
                setTimeout(() => { input.style.borderColor = ""; }, 800);
            }
        }
    };

    // Preset High-Risk Profile (Vulnerable Month-to-Month Fiber User)
    if (highRiskBtn) {
        highRiskBtn.addEventListener("click", () => {
            fillForm({
                "Gender": "Female",
                "Senior Citizen": "Yes",
                "Partner": "No",
                "Dependents": "No",
                "Tenure Months": "3",
                "Phone Service": "Yes",
                "Multiple Lines": "No",
                "Internet Service": "Fiber optic",
                "Online Security": "No",
                "Online Backup": "No",
                "Device Protection": "No",
                "Tech Support": "No",
                "Streaming TV": "Yes",
                "Streaming Movies": "Yes",
                "Contract": "Month-to-month",
                "Paperless Billing": "Yes",
                "Payment Method": "Electronic check",
                "Monthly Charges": "95.85",
                "Total Charges": "287.55",
                "CLTV": "2600"
            });
        });
    }

    // Preset Low-Risk Profile (Loyal Multi-year Auto-pay User)
    if (lowRiskBtn) {
        lowRiskBtn.addEventListener("click", () => {
            fillForm({
                "Gender": "Male",
                "Senior Citizen": "No",
                "Partner": "Yes",
                "Dependents": "Yes",
                "Tenure Months": "62",
                "Phone Service": "Yes",
                "Multiple Lines": "Yes",
                "Internet Service": "DSL",
                "Online Security": "Yes",
                "Online Backup": "Yes",
                "Device Protection": "Yes",
                "Tech Support": "Yes",
                "Streaming TV": "No",
                "Streaming Movies": "No",
                "Contract": "Two year",
                "Paperless Billing": "No",
                "Payment Method": "Bank transfer (automatic)",
                "Monthly Charges": "52.40",
                "Total Charges": "3248.80",
                "CLTV": "5600"
            });
        });
    }

    // Submit Loading State
    if (form && submitBtn) {
        form.addEventListener("submit", () => {
            submitBtn.disabled = true;
            submitBtn.innerHTML = `<span class="spinner"></span> <span>Calculating Churn Probability...</span>`;
        });
    }
});
