import pandas as pd
import numpy as np

class DataPreprocessor:

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_data(self):
        """Load dataset"""
        self.df = pd.read_csv(self.file_path)
        print("✅ Dataset Loaded Successfully")
        return self.df

    def dataset_info(self):
        """Display dataset information"""

        print("\n============ DATASET INFORMATION ================== ")
        print(f"Shape : {self.df.shape}")

        print("\nColumns:")
        print(self.df.columns.tolist())

        print("\nData TYpes:")
        print(self.df.dtypes)

    def check_missing_values(self):
        """Check missing Values"""

        print("\n================ MISSING VALUES ==================")
        print(self.df.isnull().sum())

    def check_duplicates(self):
        """Check duplicate records"""

        print("\n================= DUPLICATE RECORDS ==================")
        print(self.df.duplicated().sum())

    def save_cleaned_data(self, output_path):
        """Save cleaned dataset"""

        self.df.to_csv(output_path, index=False)
        print(f"\n✅ Cleaned dataset saved to {output_path}")