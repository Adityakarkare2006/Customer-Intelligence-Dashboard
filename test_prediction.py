from utils.prediction import CustomerPredictor

# ======================================================
# PATHS
# ======================================================

MODEL_PATH = "models/customer_model.pkl"
ENCODER_PATH = "models/label_encoders.pkl"

# ======================================================
# CREATE OBJECT
# ======================================================

predictor = CustomerPredictor(
    MODEL_PATH,
    ENCODER_PATH
)

# ======================================================
# LOAD MODEL
# ======================================================

predictor.load_model()

# ======================================================
# LOAD ENCODERS
# ======================================================

predictor.load_label_encoders()

# ======================================================
# SAMPLE CUSTOMER
# ======================================================

customer = {

    "Gender": "Male",
    "Senior Citizen": "No",
    "Partner": "Yes",
    "Dependents": "No",
    "Tenure Months": 24,
    "Phone Service": "Yes",
    "Multiple Lines": "No",
    "Internet Service": "Fiber optic",
    "Online Security": "Yes",
    "Online Backup": "No",
    "Device Protection": "Yes",
    "Tech Support": "No",
    "Streaming TV": "Yes",
    "Streaming Movies": "Yes",
    "Contract": "Month-to-month",
    "Paperless Billing": "Yes",
    "Payment Method": "Electronic check",
    "Monthly Charges": 85.75,
    "Total Charges": 2058.00,
    "CLTV": 4200

}

# ======================================================
# PREPARE DATA
# ======================================================

prepared_data = predictor.prepare_customer_data(customer)

print("\nPrepared Customer Data:\n")
print(prepared_data)

# ======================================================
# PREDICTION
# ======================================================

result = predictor.predict_customer(customer)

print("\nPrediction Result")
print("=" * 50)

print(f"Prediction     : {result['Prediction']}")
print(f"Probability    : {result['Probability']}")
print(f"Risk Level     : {result['Risk Level']}")
print(f"Recommendation : {result['Recommendation']}")

# ======================================================
# PROBABILITY
# ======================================================

probability = predictor.predict_probability(customer)

print("\nChurn Probability:")
print(f"{probability}%")