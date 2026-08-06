"""
=========================================================
        CUSTOMER INTELLIGENCE DASHBOARD
              PREDICTION MODULE
=========================================================

This Module Performs

1. Load Trained Machine Learning Model
2. Load Label Encoders
3. Prepare Customer Data
4. Predict Customer Churn
5. Predict Churn Probability

Author : Aditya Karkare (Andy)

=========================================================
"""

# =====================================================
# IMPORT LIBRARIES
# =====================================================

import joblib
import pandas as pd
from utils.insights import CustomerInsights

# =====================================================
# CUSTOMER PREDICTOR CLASS
# =====================================================

class CustomerPredictor:

    # -------------------------------------------------
    # Constructor
    # -------------------------------------------------

    def __init__(self, model_path, encoder_path):

        self.model_path = model_path
        self.encoder_path = encoder_path

        self.model = None
        self.label_encoders = None

    # -------------------------------------------------
    # Load Model
    # -------------------------------------------------

    def load_model(self):

        self.model = joblib.load(self.model_path)

        print("✅ Customer Prediction Model Loaded")

    # -------------------------------------------------
    # Load Label Encoders
    # -------------------------------------------------

    def load_label_encoders(self):

        self.label_encoders = joblib.load(self.encoder_path)

        print("✅ Label Encoders Loaded")

    # -------------------------------------------------
    # Prepare Customer Data
    # -------------------------------------------------

    def prepare_customer_data(self, customer_data):

        # Dictionary → DataFrame
        df = pd.DataFrame([customer_data])

        # Same feature order as training
        feature_order = [

            "Gender",
            "Senior Citizen",
            "Partner",
            "Dependents",
            "Tenure Months",
            "Phone Service",
            "Multiple Lines",
            "Internet Service",
            "Online Security",
            "Online Backup",
            "Device Protection",
            "Tech Support",
            "Streaming TV",
            "Streaming Movies",
            "Contract",
            "Paperless Billing",
            "Payment Method",
            "Monthly Charges",
            "Total Charges",
            "CLTV"

        ]

        df = df[feature_order]

        # Encode categorical columns
        for column in self.label_encoders.keys():

            value = str(df[column].iloc[0])

            allowed_values = self.label_encoders[column].classes_

            if value not in allowed_values:

                raise ValueError(

                    f"\nInvalid value for '{column}'\n"
                    f"Entered Value : {value}\n"
                    f"Allowed Values : {list(allowed_values)}"

                )

            df[column] = self.label_encoders[column].transform(
                df[column].astype(str)
            )

        print("✅ Customer Data Prepared Successfully")

        return df

    # -------------------------------------------------
    # Predict Customer Churn
    # -------------------------------------------------

    def predict_customer(self, customer_data):

        prepared_data = self.prepare_customer_data(customer_data)

        prediction = self.model.predict(prepared_data)

        probability = self.model.predict_proba(prepared_data)

        churn_probability = round(probability[0][1] * 100, 2)

        if prediction[0] == 1:

            prediction_text = "Customer Will Churn"

        else:

            prediction_text = "Customer Will Not Churn"

        return CustomerInsights.generate_insight(

        prediction_text,

        churn_probability

    )

    # -------------------------------------------------
    # Predict Churn Probability
    # -------------------------------------------------

    def predict_probability(self, customer_data):

        prepared_data = self.prepare_customer_data(customer_data)

        probability = self.model.predict_proba(prepared_data)

        churn_probability = probability[0][1] * 100

        return round(churn_probability, 2)