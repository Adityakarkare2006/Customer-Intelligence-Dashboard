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
6. Calculate Model Accuracy

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
        # Normalize keys if needed
        data = {}
        for k, v in customer_data.items():
            data[k.strip()] = v

        df = pd.DataFrame([data])

        # Feature order matching model training
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

        # Fill missing features with sensible defaults
        defaults = {
            "Gender": "Male",
            "Senior Citizen": "No",
            "Partner": "No",
            "Dependents": "No",
            "Tenure Months": 1,
            "Phone Service": "Yes",
            "Multiple Lines": "No",
            "Internet Service": "DSL",
            "Online Security": "No",
            "Online Backup": "No",
            "Device Protection": "No",
            "Tech Support": "No",
            "Streaming TV": "No",
            "Streaming Movies": "No",
            "Contract": "Month-to-month",
            "Paperless Billing": "Yes",
            "Payment Method": "Electronic check",
            "Monthly Charges": 50.0,
            "Total Charges": 50.0,
            "CLTV": 3000.0
        }

        for col in feature_order:
            if col not in df.columns or pd.isna(df[col].iloc[0]) or str(df[col].iloc[0]).strip() == "":
                df[col] = defaults[col]

        df = df[feature_order].copy()

        # Convert numeric columns
        numeric_cols = ["Tenure Months", "Monthly Charges", "Total Charges", "CLTV"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(defaults[col])

        # Encode categorical columns
        if self.label_encoders:
            for column, encoder in self.label_encoders.items():
                if column in df.columns:
                    val = str(df[column].iloc[0]).strip()
                    allowed_values = list(encoder.classes_)
                    
                    if val not in allowed_values:
                        # Try case-insensitive matching
                        matched = None
                        for allowed in allowed_values:
                            if allowed.lower() == val.lower():
                                matched = allowed
                                break
                        if matched:
                            val = matched
                        else:
                            val = allowed_values[0]

                    df[column] = encoder.transform([val])

        return df

    # -------------------------------------------------
    # Predict Customer Churn
    # -------------------------------------------------

    def predict_customer(self, customer_data):
        prepared_data = self.prepare_customer_data(customer_data)

        prediction = self.model.predict(prepared_data)
        probability = self.model.predict_proba(prepared_data)

        churn_probability = round(probability[0][1] * 100, 2)
        churn_class = int(prediction[0])

        if churn_class == 1 or churn_probability >= 50.0:
            prediction_text = "Customer Likely to Churn"
            will_churn = True
        else:
            prediction_text = "Customer Likely to Stay"
            will_churn = False

        contract = customer_data.get("Contract", "Month-to-month")
        payment_method = customer_data.get("Payment Method", "Electronic check")

        insight = CustomerInsights.generate_insight(
            prediction_text=prediction_text,
            churn_probability=churn_probability,
            contract=contract,
            payment_method=payment_method
        )
        insight["will_churn"] = will_churn
        insight["churn_class"] = churn_class

        return insight

    # -------------------------------------------------
    # Predict Churn Probability
    # -------------------------------------------------

    def predict_probability(self, customer_data):
        prepared_data = self.prepare_customer_data(customer_data)
        probability = self.model.predict_proba(prepared_data)
        return round(float(probability[0][1] * 100), 2)



    # =================================================
    # MODEL ACCURACY
    # =================================================

    def calculate_accuracy(self, dataset_path):

        """
        Calculate model accuracy using the
        customer churn dataset.
        """

        # ---------------------------------------------
        # Load dataset
        # ---------------------------------------------

        df = pd.read_csv(dataset_path)


        # ---------------------------------------------
        # Feature columns
        # ---------------------------------------------

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


        # ---------------------------------------------
        # Check required columns
        # ---------------------------------------------

        missing_columns = [

            column
            for column in feature_order
            if column not in df.columns

        ]


        if missing_columns:

            raise ValueError(

                "Missing feature columns: "
                + str(missing_columns)

            )


        # ---------------------------------------------
        # Prepare features
        # ---------------------------------------------

        X = df[feature_order].copy()


        # ---------------------------------------------
        # Prepare target
        # ---------------------------------------------

        if "Churn Value" in df.columns:

            y = df["Churn Value"]

        elif "Churn Label" in df.columns:

            y = (

                df["Churn Label"]
                .astype(str)
                .str.strip()
                .str.lower()
                .map({
                    "yes": 1,
                    "no": 0
                })

            )

        else:

            raise ValueError(
                "Churn target column not found."
            )


        # ---------------------------------------------
        # Encode categorical columns
        # ---------------------------------------------

        for column in self.label_encoders.keys():

            if column not in X.columns:

                continue


            X[column] = (
                self.label_encoders[column]
                .transform(
                    X[column].astype(str)
                )
            )


        # ---------------------------------------------
        # Convert numeric columns
        # ---------------------------------------------

        numeric_columns = [

            "Tenure Months",
            "Monthly Charges",
            "Total Charges",
            "CLTV"

        ]


        for column in numeric_columns:

            X[column] = pd.to_numeric(
                X[column],
                errors="coerce"
            )


        # ---------------------------------------------
        # Remove invalid rows
        # ---------------------------------------------

        valid_rows = (
            X.notna().all(axis=1)
            & y.notna()
        )


        X = X.loc[valid_rows]

        y = y.loc[valid_rows]


        # ---------------------------------------------
        # Model prediction
        # ---------------------------------------------

        predictions = self.model.predict(X)


        # ---------------------------------------------
        # Calculate accuracy
        # ---------------------------------------------

        accuracy = (
            predictions == y
        ).mean() * 100


        accuracy = round(
            accuracy,
            2
        )

        print(
            "✅ Model Accuracy:",
            accuracy,
            "%"
        )

        return accuracy

# Module-level singleton helper
_global_predictor = None

def get_default_predictor(model_path="models/customer_model.pkl", encoder_path="models/label_encoders.pkl"):
    global _global_predictor
    if _global_predictor is None:
        _global_predictor = CustomerPredictor(model_path, encoder_path)
    return _global_predictor

def predict_customer(customer_data, model_path="models/customer_model.pkl", encoder_path="models/label_encoders.pkl"):
    predictor = get_default_predictor(model_path, encoder_path)
    return predictor.predict_customer(customer_data)