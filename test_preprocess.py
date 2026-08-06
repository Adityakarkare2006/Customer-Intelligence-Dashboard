"""
=========================================================
        TEST PREPROCESSING MODULE
=========================================================

Workflow

1. Load Dataset 
2. Display Dataset Information
3. Drop Unnecessary Columns 
4. Convert Total Values
5. Handle Missing Values
6. Remove Duplicate Records
7. Save Cleaned Dataset

==========================================================
"""

from utils.preprocess import DataPreprocessor

# -------------------------------------------------------
# INPUT DATASET
# -------------------------------------------------------

INPUT_DATA_PATH = "data/raw/customer_data.csv"

# ------------------------------------------------------
# OUTPUT DATASET 
# ------------------------------------------------------

OUTPUT_DATA_PATH = "data/processed/cleaned_customer_data.csv"

def main():

    print("=" * 60)
    print(" CUSTOMER INTELLIGENCE DATA PREPROCESSING")
    print("=" * 60)

    processor = DataPreprocessor(INPUT_DATA_PATH)

    print("\nLoading Dataset...\n")
    processor.load_data()

    print("\nDataset Information...\n")
    processor.dataset_info()

    print("\nDropping Unnecessary Columns...\n")
    processor.drop_unnecessary_columns()

    print("\nConverting Total Charges...\n")
    processor.convert_total_charges()

    print("\nHandling Missing Values...\n")
    processor.handle_missing_values()

    print("\nRemoving Duplicate Record...\n")
    processor.remove_duplicates()

    print("\nSaving Clean Dataset...\n")
    processor.save_cleaned_dataset(OUTPUT_DATA_PATH)

    print("\n" + "=" * 60)
    print("PREPROCESSING COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()