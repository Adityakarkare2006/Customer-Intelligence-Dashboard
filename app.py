# ============================================================
# CUSTOMER INTELLIGENCE DASHBOARD
# FLASK APPLICATION
# ============================================================

import csv
import io
import os
import sys
import time
import random
import sqlite3
import json
from functools import wraps

import pandas as pd

from utils.data_import import (
    allowed_file,
    read_uploaded_file,
    get_column_mapping,
    validate_dataframe,
    save_uploaded_file
)

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    abort,
    jsonify,
    Response
)

from config import Config
from utils.insights import CustomerInsights
from utils.prediction import CustomerPredictor
from werkzeug.security import generate_password_hash, check_password_hash


# ============================================================
# WINDOWS UTF-8 SUPPORT
# ============================================================

if sys.platform == "win32":

    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    except Exception:
        pass


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = getattr(
    Config,
    "SECRET_KEY",
    "customer_intelligence_2026_secure_key"
)





# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATASET_PATH = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "customer_data.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "customer_model.pkl"
)

ENCODER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "label_encoders.pkl"
)

DATABASE_DIR = os.path.join(
    BASE_DIR,
    "database"
)

DATABASE_PATH = os.path.join(
    DATABASE_DIR,
    "users.db"
)

# ======================================================
# USER DATABASE
# ======================================================

def init_user_database():
    """Create user database and users table if they do not exist."""

    os.makedirs(DATABASE_DIR, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            is_verified INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

    print("✅ User database initialized")

# ============================================================
# GLOBAL VARIABLES
# ============================================================

df = pd.DataFrame()

predictor = None

_model_accuracy_cache = None


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():

    global df

    print("==============================================")
    print("LOADING CUSTOMER DATASET")
    print("==============================================")

    print("Looking for dataset at:")
    print(DATASET_PATH)

    if not os.path.exists(DATASET_PATH):

        print("❌ DATASET FILE NOT FOUND")

        df = pd.DataFrame()

        return df

    try:

        raw_df = pd.read_csv(DATASET_PATH)

        # ------------------------------------------
        # Convert numeric columns
        # ------------------------------------------

        numeric_columns = [

            "Monthly Charges",
            "Total Charges",
            "Tenure Months",
            "Churn Score",
            "CLTV",
            "Latitude",
            "Longitude",
            "Churn Value"

        ]

        for column in numeric_columns:

            if column in raw_df.columns:

                raw_df[column] = pd.to_numeric(
                    raw_df[column],
                    errors="coerce"
                )

        df = raw_df

        print("✅ DATASET FOUND")
        print("Rows:", len(df))
        print("Columns:", list(df.columns))

        return df

    except Exception as e:

        print("❌ DATASET LOAD ERROR")
        print(e)

        df = pd.DataFrame()

        return df


# ============================================================
# INITIALIZE ML MODEL
# ============================================================

def initialize_predictor():

    global predictor

    print("==============================================")
    print("LOADING MACHINE LEARNING MODEL")
    print("==============================================")

    try:

        predictor = CustomerPredictor(
            MODEL_PATH,
            ENCODER_PATH
        )

        # ------------------------------------------
        # Load model
        # ------------------------------------------

        if os.path.exists(MODEL_PATH):

            predictor.load_model()

        else:

            print("❌ MODEL FILE NOT FOUND")

        # ------------------------------------------
        # Load encoders
        # ------------------------------------------

        if os.path.exists(ENCODER_PATH):

            predictor.load_label_encoders()

        else:

            print("❌ ENCODER FILE NOT FOUND")

        print("✅ ML Model Loaded Successfully")
        print("✅ Label Encoders Loaded Successfully")

    except Exception as e:

        print("❌ ML MODEL INITIALIZATION ERROR")
        print(e)

        predictor = None


# ============================================================
# STARTUP
# ============================================================

load_dataset()

initialize_predictor()

init_user_database()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def login_required(function):

    @wraps(function)
    def decorated_function(*args, **kwargs):

        if not session.get("logged_in"):

            return redirect(
                url_for("login")
            )

        return function(*args, **kwargs)

    return decorated_function


# ============================================================
# SAFE NUMERIC
# ============================================================

def safe_numeric(value, default=0.0):

    try:

        if pd.isna(value):

            return default

        return float(value)

    except (ValueError, TypeError):

        return default


# ============================================================
# MODEL ACCURACY
# ============================================================

def calculate_model_accuracy():

    global _model_accuracy_cache

    if _model_accuracy_cache is not None:

        return _model_accuracy_cache

    if (
        predictor is None
        or predictor.model is None
        or df.empty
    ):

        return 0.0

    try:

        # ------------------------------------------
        # Target column
        # ------------------------------------------

        if "Churn Value" in df.columns:

            y_true = pd.to_numeric(
                df["Churn Value"],
                errors="coerce"
            )

        elif "Churn Label" in df.columns:

            y_true = (
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

            print("❌ Churn target column not found")

            return 0.0

        # ------------------------------------------
        # Feature columns
        # ------------------------------------------

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

        missing_columns = [

            column
            for column in feature_order
            if column not in df.columns

        ]

        if missing_columns:

            print(
                "❌ Missing model columns:",
                missing_columns
            )

            return 0.0

        # ------------------------------------------
        # Prepare features
        # ------------------------------------------

        X = df[feature_order].copy()

        y_true = y_true.loc[X.index]

        valid_mask = y_true.notna()

        X = X.loc[valid_mask]

        y_true = y_true.loc[valid_mask].astype(int)

        # ------------------------------------------
        # Encode categorical columns
        # ------------------------------------------

        if not predictor.label_encoders:

            print("❌ Label encoders not loaded")

            return 0.0

        for column, encoder in predictor.label_encoders.items():

            if column not in X.columns:

                continue

            values = X[column].astype(str)

            allowed_values = set(
                encoder.classes_
            )

            # Unknown values become NaN
            X[column] = values.apply(

                lambda value:
                encoder.transform([value])[0]
                if value in allowed_values
                else None

            )

        # ------------------------------------------
        # Numeric conversion
        # ------------------------------------------

        for column in feature_order:

            X[column] = pd.to_numeric(
                X[column],
                errors="coerce"
            )

        valid_rows = X.notna().all(axis=1)

        X = X.loc[valid_rows]

        y_true = y_true.loc[X.index]

        if X.empty:

            return 0.0

        # ------------------------------------------
        # Prediction
        # ------------------------------------------

        y_pred = predictor.model.predict(X)

        accuracy = (
            (y_pred == y_true.values).mean()
            * 100
        )

        _model_accuracy_cache = round(
            float(accuracy),
            2
        )

        print(
            "✅ Model Accuracy:",
            _model_accuracy_cache,
            "%"
        )

        return _model_accuracy_cache

    except Exception as e:

        print("❌ Accuracy calculation error:")
        print(e)

        return 0.0


# ============================================================
# DASHBOARD STATISTICS
# ============================================================

def get_dashboard_statistics():

    if df.empty:

        return {

            "total_customers": 0,
            "churned_customers": 0,
            "retained_customers": 0,
            "churn_rate": 0.0,
            "retention_rate": 0.0,
            "model_accuracy": calculate_model_accuracy(),
            "avg_monthly_charges": 0.0,
            "avg_tenure": 0.0

        }

    total_customers = len(df)

    # ------------------------------------------
    # Churn calculation
    # ------------------------------------------

    if "Churn Label" in df.columns:

        churn_values = (
            df["Churn Label"]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        churned_customers = int(
            (churn_values == "yes").sum()
        )

        retained_customers = int(
            (churn_values == "no").sum()
        )

    elif "Churn Value" in df.columns:

        churn_values = pd.to_numeric(
            df["Churn Value"],
            errors="coerce"
        )

        churned_customers = int(
            (churn_values == 1).sum()
        )

        retained_customers = int(
            (churn_values == 0).sum()
        )

    else:

        churned_customers = 0
        retained_customers = total_customers

    # ------------------------------------------
    # Rates
    # ------------------------------------------

    if total_customers > 0:

        churn_rate = round(
            (
                churned_customers
                / total_customers
            ) * 100,
            1
        )

        retention_rate = round(
            (
                retained_customers
                / total_customers
            ) * 100,
            1
        )

    else:

        churn_rate = 0.0
        retention_rate = 0.0

    # ------------------------------------------
    # Average monthly charges
    # ------------------------------------------

    if "Monthly Charges" in df.columns:

        avg_monthly_charges = round(
            safe_numeric(
                df["Monthly Charges"].mean()
            ),
            2
        )

    else:

        avg_monthly_charges = 0.0

    # ------------------------------------------
    # Average tenure
    # ------------------------------------------

    if "Tenure Months" in df.columns:

        avg_tenure = round(
            safe_numeric(
                df["Tenure Months"].mean()
            ),
            1
        )

    else:

        avg_tenure = 0.0

    return {

        "total_customers": total_customers,

        "churned_customers": churned_customers,

        "retained_customers": retained_customers,

        "churn_rate": churn_rate,

        "retention_rate": retention_rate,

        "model_accuracy": calculate_model_accuracy(),

        "avg_monthly_charges": avg_monthly_charges,

        "avg_tenure": avg_tenure

    }


# ============================================================
# HIGH RISK CUSTOMERS
# ============================================================

def get_high_risk_customers(limit=5):

    if (
        df.empty
        or "Churn Score" not in df.columns
    ):

        return []

    risk_df = df.copy()

    risk_df["Churn Score"] = pd.to_numeric(
        risk_df["Churn Score"],
        errors="coerce"
    ).fillna(0)

    risk_df = (
        risk_df
        .sort_values(
            "Churn Score",
            ascending=False
        )
        .head(limit)
    )

    results = []

    for _, row in risk_df.iterrows():

        score = int(
            round(
                safe_numeric(
                    row.get("Churn Score", 0)
                )
            )
        )

        risk_level = (
            CustomerInsights
            .get_risk_level(score)
        )

        results.append({

            "customer_id": str(
                row.get(
                    "CustomerID",
                    "N/A"
                )
            ),

            "gender": str(
                row.get(
                    "Gender",
                    "N/A"
                )
            ),

            "score": score,

            "risk_score": score,

            "risk_level": risk_level,

            "contract": str(
                row.get(
                    "Contract",
                    "N/A"
                )
            ),

            "monthly_charges": round(
                safe_numeric(
                    row.get(
                        "Monthly Charges",
                        0
                    )
                ),
                2
            ),

            "total_charges": round(
                safe_numeric(
                    row.get(
                        "Total Charges",
                        0
                    )
                ),
                2
            ),

            "tenure": int(
                safe_numeric(
                    row.get(
                        "Tenure Months",
                        0
                    )
                )
            ),

            "internet_service": str(
                row.get(
                    "Internet Service",
                    "N/A"
                )
            ),

            "payment_method": str(
                row.get(
                    "Payment Method",
                    "N/A"
                )
            ),

            "churn_label": str(
                row.get(
                    "Churn Label",
                    "No"
                )
            )

        })

    return results


# ============================================================
# HIGH RISK SEGMENT
# ============================================================

def get_high_risk_segment():

    if (
        df.empty
        or "Contract" not in df.columns
        or "Churn Label" not in df.columns
    ):

        return {

            "segment": "Month-to-month",

            "score": 0.0,

            "message":
                "Month-to-month customers show "
                "high churn vulnerability."

        }

    temp_df = df.copy()

    temp_df["Churn"] = (

        temp_df["Churn Label"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map({
            "yes": 1,
            "no": 0
        })

    )

    temp_df = temp_df.dropna(
        subset=[
            "Contract",
            "Churn"
        ]
    )

    if temp_df.empty:

        return {

            "segment": "Month-to-month",

            "score": 0.0,

            "message":
                "Month-to-month customers show "
                "high churn vulnerability."

        }

    grouped = (
        temp_df
        .groupby("Contract")["Churn"]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    top_segment = grouped.index[0]

    top_rate = round(
        float(grouped.iloc[0] * 100),
        1
    )

    return {

        "segment": top_segment,

        "score": top_rate,

        "message":
            f"{top_segment} customers have "
            f"the highest churn rate "
            f"({top_rate}%)."

    }


# ============================================================
# DYNAMIC INSIGHTS
# ============================================================

def get_dynamic_insights():

    insights = []

    if df.empty:

        return [

            {

                "type": "info",

                "icon":
                    "ri-information-line",

                "title":
                    "Dataset Ready",

                "message":
                    "Customer dataset is not available."

            }

        ]

    # ------------------------------------------
    # Insight 1
    # ------------------------------------------

    if (
        "Contract" in df.columns
        and "Churn Label" in df.columns
    ):

        m2m = df[
            df["Contract"]
            .astype(str)
            .str.strip()
            == "Month-to-month"
        ]

        if len(m2m) > 0:

            churned = (

                m2m["Churn Label"]
                .astype(str)
                .str.strip()
                .str.lower()
                == "yes"

            ).sum()

            rate = round(
                (churned / len(m2m)) * 100,
                1
            )

            insights.append({

                "type": "warning",

                "icon":
                    "ri-error-warning-line",

                "title":
                    "Month-to-Month Risk",

                "message":
                    f"Month-to-month customers "
                    f"have a {rate}% churn rate."

            })

    # ------------------------------------------
    # Insight 2
    # ------------------------------------------

    if "Churn Score" in df.columns:

        scores = pd.to_numeric(
            df["Churn Score"],
            errors="coerce"
        )

        high_risk_count = int(
            (scores >= 80).sum()
        )

        percentage = round(
            (
                high_risk_count
                / len(df)
            ) * 100,
            1
        )

        insights.append({

            "type": "danger",

            "icon":
                "ri-alarm-warning-line",

            "title":
                "High Risk Customers",

            "message":
                f"{high_risk_count:,} customers "
                f"({percentage}%) have "
                f"a churn score of 80 or above."

        })

    # ------------------------------------------
    # Insight 3
    # ------------------------------------------

    if (
        "Payment Method" in df.columns
        and "Churn Label" in df.columns
    ):

        electronic = df[
            df["Payment Method"]
            .astype(str)
            .str.strip()
            == "Electronic check"
        ]

        if len(electronic) > 0:

            churned = (

                electronic["Churn Label"]
                .astype(str)
                .str.strip()
                .str.lower()
                == "yes"

            ).sum()

            rate = round(
                (churned / len(electronic)) * 100,
                1
            )

            insights.append({

                "type": "info",

                "icon":
                    "ri-bank-card-line",

                "title":
                    "Payment Method Insight",

                "message":
                    f"Electronic check users "
                    f"have a churn rate of {rate}%."

            })

    # ------------------------------------------
    # Insight 4
    # ------------------------------------------

    segment = get_high_risk_segment()

    insights.append({

        "type": "success",

        "icon":
            "ri-lightbulb-line",

        "title":
            "Retention Recommendation",

        "message":
            f"Focus retention campaigns "
            f"on {segment['segment']} customers."

    })

    return insights


# ============================================================
# ANALYTICS DATA
# ============================================================

def get_analytics_data():

    stats = get_dashboard_statistics()

    analytics = {

        "churned":
            stats["churned_customers"],

        "retained":
            stats["retained_customers"],

        "total":
            stats["total_customers"],

        "churn_rate":
            stats["churn_rate"],

        "retention_rate":
            stats["retention_rate"],

        "avg_monthly_charges":
            stats["avg_monthly_charges"],

        "avg_tenure":
            stats["avg_tenure"],

        "month_to_month": 0,

        "one_year": 0,

        "two_year": 0,

        "electronic_check": 0,

        "mailed_check": 0,

        "bank_transfer": 0,

        "credit_card": 0,

        "dsl": 0,

        "fiber_optic": 0,

        "no_internet": 0,

        "churn_by_contract": {},

        "churn_by_tenure": {}

    }

    if df.empty:

        return analytics

    # ------------------------------------------
    # Contract
    # ------------------------------------------

    if "Contract" in df.columns:

        contracts = (
            df["Contract"]
            .astype(str)
            .str.strip()
        )

        analytics["month_to_month"] = int(
            (contracts == "Month-to-month").sum()
        )

        analytics["one_year"] = int(
            (contracts == "One year").sum()
        )

        analytics["two_year"] = int(
            (contracts == "Two year").sum()
        )

    # ------------------------------------------
    # Payment Method
    # ------------------------------------------

    if "Payment Method" in df.columns:

        payment = (
            df["Payment Method"]
            .astype(str)
            .str.strip()
        )

        analytics["electronic_check"] = int(
            (payment == "Electronic check").sum()
        )

        analytics["mailed_check"] = int(
            (payment == "Mailed check").sum()
        )

        analytics["bank_transfer"] = int(
            (
                payment
                == "Bank transfer (automatic)"
            ).sum()
        )

        analytics["credit_card"] = int(
            (
                payment
                == "Credit card (automatic)"
            ).sum()
        )

    # ------------------------------------------
    # Internet Service
    # ------------------------------------------

    if "Internet Service" in df.columns:

        internet = (
            df["Internet Service"]
            .astype(str)
            .str.strip()
        )

        analytics["dsl"] = int(
            (internet == "DSL").sum()
        )

        analytics["fiber_optic"] = int(
            (internet == "Fiber optic").sum()
        )

        analytics["no_internet"] = int(
            (internet == "No").sum()
        )

    # ------------------------------------------
    # Churn by Contract
    # ------------------------------------------

    if (
        "Contract" in df.columns
        and "Churn Label" in df.columns
    ):

        for contract in [

            "Month-to-month",
            "One year",
            "Two year"

        ]:

            subset = df[
                df["Contract"]
                .astype(str)
                .str.strip()
                == contract
            ]

            churned = int(
                (
                    subset["Churn Label"]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    == "yes"
                ).sum()
            )

            retained = int(
                (
                    subset["Churn Label"]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    == "no"
                ).sum()
            )

            analytics[
                "churn_by_contract"
            ][contract] = {

                "churned": churned,
                "retained": retained,

                "Yes": churned,
                "No": retained

            }

    # ------------------------------------------
    # Churn by Tenure
    # ------------------------------------------

    if (
        "Tenure Months" in df.columns
        and "Churn Label" in df.columns
    ):

        tenure = pd.to_numeric(
            df["Tenure Months"],
            errors="coerce"
        ).fillna(0)

        churn = (

            df["Churn Label"]
            .astype(str)
            .str.strip()
            .str.lower()
            == "yes"

        )

        groups = [

            (
                "0-12 Months",
                tenure <= 12
            ),

            (
                "13-24 Months",
                (tenure > 12)
                & (tenure <= 24)
            ),

            (
                "25-48 Months",
                (tenure > 24)
                & (tenure <= 48)
            ),

            (
                "49-72 Months",
                tenure > 48
            )

        ]

        for label, mask in groups:

            churned = int(
                (mask & churn).sum()
            )

            retained = int(
                (mask & ~churn).sum()
            )

            analytics[
                "churn_by_tenure"
            ][label] = {

                "churned": churned,
                "retained": retained,

                "Yes": churned,
                "No": retained

            }

    # ------------------------------------------
    # JS Friendly Data
    # ------------------------------------------

    analytics["contracts"] = {

        "Month-to-month":
            analytics["month_to_month"],

        "One year":
            analytics["one_year"],

        "Two year":
            analytics["two_year"]

    }

    analytics["payment_methods"] = {

        "Electronic check":
            analytics["electronic_check"],

        "Mailed check":
            analytics["mailed_check"],

        "Bank transfer (auto)":
            analytics["bank_transfer"],

        "Credit card (auto)":
            analytics["credit_card"]

    }

    analytics["internet_services"] = {

        "Fiber optic":
            analytics["fiber_optic"],

        "DSL":
            analytics["dsl"],

        "No internet":
            analytics["no_internet"]

    }

    return analytics


# ============================================================
# SERIALIZE CUSTOMER
# ============================================================

def serialize_customer(row):

    score = int(
        round(
            safe_numeric(
                row.get(
                    "Churn Score",
                    0
                )
            )
        )
    )

    return {

        "CustomerID":
            str(row.get(
                "CustomerID",
                "N/A"
            )),

        "Gender":
            str(row.get(
                "Gender",
                "N/A"
            )),

        "Senior Citizen":
            str(row.get(
                "Senior Citizen",
                "No"
            )),

        "Partner":
            str(row.get(
                "Partner",
                "No"
            )),

        "Dependents":
            str(row.get(
                "Dependents",
                "No"
            )),

        "Tenure Months":
            int(
                safe_numeric(
                    row.get(
                        "Tenure Months",
                        0
                    )
                )
            ),

        "Phone Service":
            str(row.get(
                "Phone Service",
                "Yes"
            )),

        "Multiple Lines":
            str(row.get(
                "Multiple Lines",
                "No"
            )),

        "Internet Service":
            str(row.get(
                "Internet Service",
                "No"
            )),

        "Online Security":
            str(row.get(
                "Online Security",
                "No"
            )),

        "Online Backup":
            str(row.get(
                "Online Backup",
                "No"
            )),

        "Device Protection":
            str(row.get(
                "Device Protection",
                "No"
            )),

        "Tech Support":
            str(row.get(
                "Tech Support",
                "No"
            )),

        "Streaming TV":
            str(row.get(
                "Streaming TV",
                "No"
            )),

        "Streaming Movies":
            str(row.get(
                "Streaming Movies",
                "No"
            )),

        "Contract":
            str(row.get(
                "Contract",
                "Month-to-month"
            )),

        "Paperless Billing":
            str(row.get(
                "Paperless Billing",
                "Yes"
            )),

        "Payment Method":
            str(row.get(
                "Payment Method",
                "Electronic check"
            )),

        "Monthly Charges":
            round(
                safe_numeric(
                    row.get(
                        "Monthly Charges",
                        0
                    )
                ),
                2
            ),

        "Total Charges":
            round(
                safe_numeric(
                    row.get(
                        "Total Charges",
                        0
                    )
                ),
                2
            ),

        "CLTV":
            int(
                safe_numeric(
                    row.get(
                        "CLTV",
                        0
                    )
                )
            ),

        "Churn Label":
            str(row.get(
                "Churn Label",
                "No"
            )),

        "Churn Score":
            score,

        "Risk Level":
            CustomerInsights.get_risk_level(
                score
            ),

        "City":
            str(row.get(
                "City",
                "N/A"
            )),

        "State":
            str(row.get(
                "State",
                "N/A"
            )),

        "Zip Code":
            str(row.get(
                "Zip Code",
                "N/A"
            )),

        "Churn Reason":
            str(
                row.get(
                    "Churn Reason",
                    "N/A"
                )
            )
            if pd.notna(
                row.get(
                    "Churn Reason",
                    None
                )
            )
            else "None"

    }


# ============================================================
# GET CUSTOMER BY ID
# ============================================================

def get_customer_by_id(customer_id):

    if (
        df.empty
        or "CustomerID" not in df.columns
    ):

        return None

    matched = df[
        df["CustomerID"]
        .astype(str)
        .str.strip()
        .str.upper()
        ==
        str(customer_id)
        .strip()
        .upper()
    ]

    if matched.empty:

        return None

    return serialize_customer(
        matched.iloc[0]
    )

# ======================================================
# SIGNUP ROUTE
# ======================================================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if session.get("logged_in"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        terms = request.form.get("terms")

        form_data = {
            "full_name": full_name,
            "email": email,
            "username": username
        }

        # Validation
        if not full_name or not email or not username or not password:
            return render_template(
                "signup.html",
                error="Please fill in all required fields.",
                form_data=form_data
            )

        if not terms:
            return render_template(
                "signup.html",
                error="Please accept the Terms & Conditions.",
                form_data=form_data
            )

        if len(password) < 6:
            return render_template(
                "signup.html",
                error="Password must contain at least 6 characters.",
                form_data=form_data
            )

        if password != confirm_password:
            return render_template(
                "signup.html",
                error="Passwords do not match.",
                form_data=form_data
            )

        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()

        # Check existing email
        cursor.execute(
            "SELECT id FROM users WHERE email = ?",
            (email,)
        )

        existing_email = cursor.fetchone()

        if existing_email:
            connection.close()

            return render_template(
                "signup.html",
                error="An account with this email already exists.",
                form_data=form_data
            )

        # Check existing username
        cursor.execute(
            "SELECT id FROM users WHERE username = ?",
            (username,)
        )

        existing_username = cursor.fetchone()

        if existing_username:
            connection.close()

            return render_template(
                "signup.html",
                error="Username is already taken.",
                form_data=form_data
            )

        # Hash password
        password_hash = generate_password_hash(password)

        # Create user
        cursor.execute(
            """
            INSERT INTO users
            (full_name, email, username, password_hash, is_verified)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                full_name,
                email,
                username,
                password_hash,
                0
            )
        )

        connection.commit()

        user_id = cursor.lastrowid

        connection.close()

        # Generate OTP
        import random

        otp = str(random.randint(100000, 999999))

        session["signup_user_id"] = user_id
        session["signup_otp"] = otp
        session["signup_otp_created_at"] = time.time()

        print("\n" + "=" * 55)
        print("🔐 SIGNUP OTP GENERATED")
        print("Username:", username)
        print("Email:", email)
        print("OTP:", otp)
        print("Valid for: 2 minutes")
        print("=" * 55 + "\n")

        return redirect(url_for("verify_signup"))

    return render_template(
        "signup.html",
        form_data={}
    )
# ======================================================
# SIGNUP OTP VERIFICATION
# ======================================================

@app.route("/verify-signup", methods=["GET", "POST"])
def verify_signup():

    if "signup_otp" not in session:
        return redirect(url_for("signup"))

    if request.method == "POST":

        entered_otp = request.form.get("otp", "").strip()

        correct_otp = session.get("signup_otp")

        created_at = session.get(
            "signup_otp_created_at",
            0
        )

        # OTP expires after 2 minutes
        if time.time() - created_at > 120:

            session.pop("signup_otp", None)
            session.pop("signup_otp_created_at", None)
            session.pop("signup_user_id", None)

            return render_template(
                "verify_signup.html",
                error="OTP has expired. Please register again."
            )

        if entered_otp != correct_otp:

            return render_template(
                "verify_signup.html",
                error="Invalid OTP. Please try again."
            )

        user_id = session.get("signup_user_id")

        connection = sqlite3.connect(DATABASE_PATH)

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE users
            SET is_verified = 1
            WHERE id = ?
            """,
            (user_id,)
        )

        connection.commit()
        connection.close()

        # Clear signup session
        session.pop("signup_otp", None)
        session.pop("signup_otp_created_at", None)
        session.pop("signup_user_id", None)

        return redirect(url_for("login"))

    return render_template("verify_signup.html")

# ============================================================
# LOGIN
# ============================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if session.get("logged_in"):

        return redirect(
            url_for("dashboard")
        )

    if request.method == "POST":

        username = (
            request.form
            .get("username", "")
            .strip()
        )

        password = (
            request.form
            .get("password", "")
            .strip()
        )

        if (
            username == "admin"
            and password == "admin123"
        ):

            otp = str(
                random.randint(
                    100000,
                    999999
                )
            )

            session["otp"] = otp

            session["otp_verified"] = False

            session["login_username"] = username

            session["otp_created_at"] = time.time()

            print("\n" + "=" * 50)
            print("🔐 DEMO OTP GENERATED")
            print("OTP:", otp)
            print("Valid for: 2 minutes")
            print("=" * 50 + "\n")

            return redirect(
                url_for("verify_otp")
            )

        return render_template(
            "login.html",
            error="Invalid username or password."
        )

    return render_template(
        "login.html"
    )


# ============================================================
# OTP VERIFICATION
# ============================================================

@app.route(
    "/verify-otp",
    methods=["GET", "POST"]
)
def verify_otp():

    if "otp" not in session:

        return redirect(
            url_for("login")
        )

    if request.method == "POST":

        entered_otp = (
            request.form
            .get("otp", "")
            .strip()
        )

        correct_otp = session.get(
            "otp"
        )

        created_at = session.get(
            "otp_created_at",
            0
        )

        # ------------------------------------------
        # OTP expiry
        # ------------------------------------------

        if time.time() - created_at > 120:

            session.pop("otp", None)

            session.pop(
                "otp_created_at",
                None
            )

            return render_template(
                "otp.html",
                error="OTP expired. Please request a new OTP."
            )

        # ------------------------------------------
        # OTP verification
        # ------------------------------------------

        if entered_otp == correct_otp:

            session["logged_in"] = True

            session["otp_verified"] = True

            session.pop(
                "otp",
                None
            )

            session.pop(
                "otp_created_at",
                None
            )

            return redirect(
                url_for("dashboard")
            )

        return render_template(
            "otp.html",
            error="Invalid OTP. Please try again."
        )

    return render_template(
        "otp.html"
    )


# ============================================================
# RESEND OTP
# ============================================================

@app.route("/resend-otp")
def resend_otp():

    if "login_username" not in session:

        return redirect(
            url_for("login")
        )

    otp = str(
        random.randint(
            100000,
            999999
        )
    )

    session["otp"] = otp

    session["otp_verified"] = False

    session["otp_created_at"] = time.time()

    print("\n" + "=" * 50)
    print("🔄 NEW DEMO OTP GENERATED")
    print("OTP:", otp)
    print("Valid for: 2 minutes")
    print("=" * 50 + "\n")

    return redirect(
        url_for("verify_otp")
    )


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/")
@login_required
def dashboard():

    stats = get_dashboard_statistics()

    high_risk_customers = (
        get_high_risk_customers(
            limit=5
        )
    )

    high_risk_segment = (
        get_high_risk_segment()
    )

    dynamic_insights = (
        get_dynamic_insights()
    )

    recent_predictions = (
        session.get(
            "recent_predictions",
            []
        )
    )

    return render_template(

        "dashboard.html",

        total_customers=
            stats["total_customers"],

        churned_customers=
            stats["churned_customers"],

        retained_customers=
            stats["retained_customers"],

        churn_rate=
            stats["churn_rate"],

        retention_rate=
            stats["retention_rate"],

        model_accuracy=
            stats["model_accuracy"],

        avg_monthly_charges=
            stats["avg_monthly_charges"],

        avg_tenure=
            stats["avg_tenure"],

        high_risk_customers=
            high_risk_customers,

        high_risk_segment=
            high_risk_segment,

        insights=
            dynamic_insights,

        recent_customers=
            recent_predictions

    )


# ============================================================
# CUSTOMERS
# ============================================================

@app.route("/customers")
@login_required
def customers():

    stats = get_dashboard_statistics()

    customers_data = []

    if not df.empty:

        customer_df = df.copy()

        for column in [

            "Churn Score",
            "Monthly Charges",
            "Total Charges",
            "Tenure Months"

        ]:

            if column in customer_df.columns:

                customer_df[column] = pd.to_numeric(
                    customer_df[column],
                    errors="coerce"
                ).fillna(0)

        for _, row in customer_df.iterrows():

            customers_data.append(
                serialize_customer(row)
            )

    return render_template(

        "customer.html",

        customers=
            customers_data,

        total_customers=
            stats["total_customers"],

        churned_customers=
            stats["churned_customers"],

        retained_customers=
            stats["retained_customers"],

        churn_rate=
            stats["churn_rate"]

    )


# ============================================================
# CUSTOMER DETAIL
# ============================================================

@app.route(
    "/customer/<customer_id>"
)
@login_required
def customer_detail(customer_id):

    customer = get_customer_by_id(
        customer_id
    )

    if not customer:

        abort(404)

    prediction_result = None

    if (
        predictor
        and predictor.model
    ):

        try:

            prediction_result = (
                predictor.predict_customer(
                    customer
                )
            )

        except Exception as e:

            print(
                f"[Prediction Error] {e}"
            )

    return render_template(

        "customer_detail.html",

        customer=
            customer,

        prediction=
            prediction_result

    )

@app.route("/data-import", methods=["GET", "POST"])
@login_required
def data_import():

    if request.method == "POST":

        uploaded_file = request.files.get("file")

        if not uploaded_file or uploaded_file.filename == "":
            return render_template(
                "data_import.html",
                error="Please select a CSV or Excel file."
            )

        try:
            # File type check
            if not allowed_file(uploaded_file.filename):
                raise ValueError(
                    "Only CSV and Excel (.xlsx) files are allowed."
                )

            # Read uploaded file
            df_import = read_uploaded_file(uploaded_file)

            # Validate data
            validation_errors = validate_dataframe(df_import)

            if validation_errors:
                return render_template(
                    "data_import.html",
                    error="; ".join(validation_errors)
                )

            # Save original uploaded file
            upload_folder = os.path.join(
                app.root_path,
                "data",
                "uploads"
            )

            file_path = save_uploaded_file(
                uploaded_file,
                upload_folder
            )

            # Get columns for mapping
            mapping = get_column_mapping(df_import)

            # Preview first 10 rows
            preview = df_import.head(10).fillna("").to_dict(
                orient="records"
            )

            return render_template(
                "data_import.html",
                success="File uploaded successfully.",
                filename=os.path.basename(file_path),
                columns=mapping["uploaded_columns"],
                system_fields=mapping["system_fields"],
                preview=preview
            )

        except Exception as e:
            print("[Data Import Error]", e)

            return render_template(
                "data_import.html",
                error=str(e)
            )

    return render_template("data_import.html")

# ============================================================
# PREDICTION
# ============================================================

@app.route("/prediction", methods=["GET", "POST"])
@login_required
def prediction():

    prediction_result = None
    prediction_error = None
    form_data = {}

    if request.method == "POST":

        form_data = request.form.to_dict()

        if not predictor or not predictor.model:

            prediction_error = (
                "Machine Learning model is not available."
            )

        else:

            try:

                insight = predictor.predict_customer(form_data)

                prediction_result = insight

                recent = session.get(
                    "recent_predictions",
                    []
                )

                recent_entry = {
                    "customer_id": f"PRED-{len(recent)+1:04d}",

                    "contract": form_data.get(
                        "Contract",
                        "Month-to-month"
                    ),

                    "monthly_charges": round(
                        safe_numeric(
                            form_data.get(
                                "Monthly Charges",
                                0
                            )
                        ),
                        2
                    ),

                    "prediction": insight.get(
                        "prediction",
                        "Unknown"
                    ),

                    "risk_score": insight.get(
                        "risk_score",
                        0
                    ),

                    "status_class": (
                        "status-churn"
                        if insight.get("will_churn", False)
                        else "status-retained"
                    )
                }

                recent.insert(0, recent_entry)

                session["recent_predictions"] = recent[:10]
                session.modified = True

            except Exception as e:

                prediction_error = (
                    f"Unable to generate prediction: {str(e)}"
                )

                print(
                    "[Prediction Route Error]",
                    e
                )

    return render_template(
        "prediction.html",
        prediction_result=prediction_result,
        prediction_error=prediction_error,
        form_data=form_data,
        model_accuracy=calculate_model_accuracy()
    )


# ============================================================
# PREDICTION API
# ============================================================

@app.route(
    "/api/predict",
    methods=["POST"]
)
@login_required
def api_predict():

    if (
        not predictor
        or not predictor.model
    ):

        return jsonify({

            "success": False,

            "error":
                "ML model is offline"

        }), 503

    try:

        data = (
            request.get_json(
                silent=True
            )
            or request.form.to_dict()
        )

        if not data:

            return jsonify({

                "success": False,

                "error":
                    "No input features provided"

            }), 400

        insight = (
            predictor.predict_customer(
                data
            )
        )

        return jsonify({

            "success": True,

            "prediction":
                insight.get(
                    "prediction"
                ),

            "probability":
                insight.get(
                    "probability"
                ),

            "risk_score":
                insight.get(
                    "risk_score"
                ),

            "risk_level":
                insight.get(
                    "risk_level"
                ),

            "recommendation":
                insight.get(
                    "recommendation"
                ),

            "will_churn":
                insight.get(
                    "will_churn",
                    False
                )

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 400


# ============================================================
# ANALYTICS
# ============================================================

@app.route("/analytics")
@login_required
def analytics():

    analytics_data = (
        get_analytics_data()
    )

    return render_template(

        "analytics.html",

        analytics=
            analytics_data,

        model_accuracy=
            calculate_model_accuracy()

    )


# ============================================================
# REPORTS
# ============================================================

@app.route("/reports")
@login_required
def reports():

    stats = get_dashboard_statistics()

    analytics = get_analytics_data()

    high_risk_count = 0
    medium_risk_count = 0
    low_risk_count = 0

    if (
        not df.empty
        and "Churn Score" in df.columns
    ):

        scores = pd.to_numeric(
            df["Churn Score"],
            errors="coerce"
        ).fillna(0)

        high_risk_count = int(
            (scores >= 80).sum()
        )

        medium_risk_count = int(
            (
                (scores >= 60)
                & (scores < 80)
            ).sum()
        )

        low_risk_count = int(
            (scores < 60).sum()
        )

    total = stats[
        "total_customers"
    ]

    return render_template(

        "reports.html",

        report={

            "total_customers":
                stats["total_customers"],

            "churned_customers":
                stats["churned_customers"],

            "retained_customers":
                stats["retained_customers"],

            "churn_rate":
                stats["churn_rate"],

            "retention_rate":
                stats["retention_rate"],

            "model_accuracy":
                stats["model_accuracy"],

            "avg_monthly_charges":
                stats["avg_monthly_charges"],

            "avg_tenure":
                stats["avg_tenure"],

            "high_risk_count":
                high_risk_count,

            "high_risk_pct":
                round(
                    (
                        high_risk_count
                        / total
                    ) * 100,
                    1
                )
                if total > 0
                else 0,

            "med_risk_count":
                medium_risk_count,

            "med_risk_pct":
                round(
                    (
                        medium_risk_count
                        / total
                    ) * 100,
                    1
                )
                if total > 0
                else 0,

            "low_risk_count":
                low_risk_count,

            "low_risk_pct":
                round(
                    (
                        low_risk_count
                        / total
                    ) * 100,
                    1
                )
                if total > 0
                else 0,

            "month_to_month":
                analytics[
                    "month_to_month"
                ],

            "one_year":
                analytics[
                    "one_year"
                ],

            "two_year":
                analytics[
                    "two_year"
                ],

            "electronic_check":
                analytics[
                    "electronic_check"
                ],

            "mailed_check":
                analytics[
                    "mailed_check"
                ],

            "bank_transfer":
                analytics[
                    "bank_transfer"
                ],

            "credit_card":
                analytics[
                    "credit_card"
                ],

            "top_high_risk_customers":
                get_high_risk_customers(
                    limit=10
                )

        }

    )


# ============================================================
# CSV EXPORT
# ============================================================

@app.route(
    "/reports/export/csv"
)
@login_required
def export_csv():

    if df.empty:

        return (
            "Dataset is not available.",
            404
        )

    output = io.StringIO()

    writer = csv.writer(
        output
    )

    writer.writerow(
        df.columns.tolist()
    )

    for _, row in df.iterrows():

        writer.writerow(
            row.tolist()
        )

    output.seek(0)

    return Response(

        output.getvalue(),

        mimetype="text/csv",

        headers={

            "Content-Disposition":
                "attachment; "
                "filename="
                "customer_intelligence_report.csv"

        }

    )


# ============================================================
# PROFILE
# ============================================================

@app.route("/profile")
@login_required
def profile():

    stats = (
        get_dashboard_statistics()
    )

    return render_template(

        "profile.html",

        stats=stats

    )


# ============================================================
# SETTINGS
# ============================================================

@app.route("/settings")
@login_required
def settings():

    return render_template(
        "settings.html"
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "404.html"
    ), 404


@app.errorhandler(500)
def server_error(error):

    return render_template(
        "500.html"
    ), 500


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    host = getattr(
        Config,
        "HOST",
        "0.0.0.0"
    )

    port = getattr(
        Config,
        "PORT",
        5000
    )

    debug = getattr(
        Config,
        "DEBUG",
        True
    )

    print("==============================================")
    print("       CUSTOMER INTELLIGENCE DASHBOARD       ")
    print("==============================================")
    print(
        f"       Running on http://{host}:{port}"
    )
    print("==============================================")

    app.run(

        host=host,

        port=port,

        debug=debug

    )