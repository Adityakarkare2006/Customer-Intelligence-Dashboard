"""
=======================================================
    CUSTOMER INTELLIGENCE DASHBOARD
            ENCODING MODULE
=======================================================

This Module performs:

1. Load Cleaned Dataset
2. Encode Categorical Columns
3. Save Label Encoders
4. Save Encoded Dataset

Author : Aditya Karkare (Andy)
=======================================================
"""

import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder


class DataEncoder:

    def __init__(self, input_path):
        self.input_path = input_path
        self.df = None
        self.label_encoders = {}

    # -----------------------------------------------------
    # Load Dataset
    # -----------------------------------------------------

    def load_data(self):

        self.df = pd.read_csv(self.input_path)

        print("✅ Cleaned Dataset Loaded Successfully")
        print(f"Dataset Shape : {self.df.shape}")

        return self.df

    # ------------------------------------------------------
    # Encode Categorical Columns
    # ------------------------------------------------------

    def encode_categorical_columns(self):

        categorical_columns = self.df.select_dtypes(include="object").columns

        print("\nEncoding Columns...\n")

        for column in categorical_columns:

            encoder = LabelEncoder()

            self.df[column] = encoder.fit_transform(
                self.df[column].astype(str)
            )

            self.label_encoders[column] = encoder

            print(f"✔ {column} Encoded")

        print("\n✅ All Categorical Columns Encoded Successfully")

    # ------------------------------------------------------
    # Save Label Encoders
    # ------------------------------------------------------

    def save_encoders(self, output_path):

        joblib.dump(self.label_encoders, output_path)

        print("\n✅ Label Encoders Saved Successfully")
        print(output_path)

    # ------------------------------------------------------
    # Save Encoded Dataset
    # ------------------------------------------------------

    def save_encoded_dataset(self, output_path):

        self.df.to_csv(output_path, index=False)

        print("\n✅ Encoded Dataset Saved Successfully")
        print(output_path)