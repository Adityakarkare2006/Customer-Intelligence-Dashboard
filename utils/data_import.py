import os
import pandas as pd
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {"csv", "xlsx"}


def allowed_file(filename):
    """Check whether the uploaded file has an allowed extension."""
    if not filename or "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS


def read_uploaded_file(file):
    """Read CSV or Excel file into a pandas DataFrame."""

    filename = secure_filename(file.filename)

    if not allowed_file(filename):
        raise ValueError("Only CSV and Excel (.xlsx) files are allowed.")

    extension = filename.rsplit(".", 1)[1].lower()

    if extension == "csv":
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    if df.empty:
        raise ValueError("The uploaded file is empty.")

    # Remove completely empty rows and columns
    df = df.dropna(axis=0, how="all")
    df = df.dropna(axis=1, how="all")

    if df.empty:
        raise ValueError("No usable data was found in the uploaded file.")

    return df


def get_column_mapping(df):
    """
    Return uploaded columns and system-supported customer fields.
    """

    system_fields = [
        "CustomerID",
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
        "CLTV",
        "Churn Label",
        "Churn Score",
        "City",
        "State",
        "Zip Code",
        "Churn Reason"
    ]

    return {
        "uploaded_columns": list(df.columns),
        "system_fields": system_fields
    }


def validate_dataframe(df):
    """Basic validation before importing customer data."""

    errors = []

    if df.empty:
        errors.append("The uploaded file contains no data.")

    if len(df.columns) == 0:
        errors.append("The uploaded file contains no columns.")

    duplicate_columns = df.columns[df.columns.duplicated()].tolist()

    if duplicate_columns:
        errors.append(
            f"Duplicate columns found: {duplicate_columns}"
        )

    return errors


def save_uploaded_file(file, upload_folder):
    """Save the original uploaded file safely."""

    if not file or not file.filename:
        raise ValueError("No file was selected.")

    filename = secure_filename(file.filename)

    if not allowed_file(filename):
        raise ValueError(
            "Invalid file type. Please upload CSV or Excel (.xlsx)."
        )

    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, filename)

    file.save(file_path)

    return file_path