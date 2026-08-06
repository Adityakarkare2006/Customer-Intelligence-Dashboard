"""
=======================================================
    CUSTOMERS INTELLIGENCE DASHBOARD
        DATA PREPROCESSING MODULE
=======================================================

This module performs:

1. Load Raw Dataset 
2. Drop Unnecessary Columns 
3. Convert Total Charges To Numberic
4. Handle Missing Values 
5. Remove Duplicates Records
6. Save Cleaned Dataset

Author : Aditya Karkare (Andy)
=======================================================
"""

import pandas as pd 


class DataPreprocessor:
    def __init__(self, input_path):
        self.input_path = input_path
        self.df = None

    # -------------------------------------------------------
    # Load Dataset
    # -------------------------------------------------------

    def load_data(self):
        self.df = pd.read_csv(self.input_path)

        print("✅ Dataset Loaded Successfully")
        print(f"Dataset Shape : {self.df.shape}")

        return self.df

    # --------------------------------------------------------
    # Dataset Information
    # --------------------------------------------------------

    def dataset_info(self):

        print("\n======= DATASET INFORMATION =========")
        self.df.info()

    # --------------------------------------------------------
    # Drop Unnecessary Columns
    # --------------------------------------------------------

    def drop_unnecessary_columns(self):

        columns_to_drop = [
            "CustomerID",
            "Count",
            "Country",
            "State",
            "City",
            "Zip Code",
            "Lat Long",
            "Latitude",
            "Longitude",
            "Churn Label",
            "Churn Score",
            "Churn Reason"
        ]

        self.df.drop(columns=columns_to_drop, inplace=True)

        print("\n✅ Unnecessary Columns Removed")

    # ----------------------------------------------
    # Convert Total Charges 
    # ----------------------------------------------

    def convert_total_charges(self):
        self.df["Total Charges"] = pd.to_numeric(
            self.df["Total Charges"],
            errors="coerce"
        )

        print("\n✅ Total Charges Converted To Numeric")

    # -----------------------------------------------------
    # Handle Missing Values
    # -----------------------------------------------------

    def handle_missing_values(self):

        print("\n Missing Values Before")
        print(self.df.isnull().sum())

        self.df.dropna(inplace=True)

        print("\nMissing Values After")
        print(self.df.isnull().sum())

        print("\n✅ Missing Values Removed")


    # ----------------------------------------------------
    # Removes Duplicate Records
    # ----------------------------------------------------

    def remove_duplicates(self):

        before = self.df.shape[0]

        self.df.drop_duplicates(inplace=True)

        after = self.df.shape[0]

        print(f"\n✅ Removed {before-after} Duplicate Rows")


    # -----------------------------------------------------
    # Save Clean Forest
    # -----------------------------------------------------

    def save_cleaned_dataset(self, output_path):

        self.df.to_csv(output_path, index=False)

        print("\n✅ Cleaned Dataset Saved Successfully")
        print(output_path)