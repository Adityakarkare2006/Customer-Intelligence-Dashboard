"""
=========================================================
    TEST ENCODING MODULE
=========================================================

Workflow:

1. Load Cleaned Dataset
2. Encode Categorical Columns
3. Save Label Encoders
4. Save Encoded Dataset

=========================================================
"""

from utils.encoding import DataEncoder

# -------------------------------------------------------
# INPUT DATASET PATH
# -------------------------------------------------------

INPUT_DATA_PATH = "data/processed/cleaned_customer_data.csv"

# -------------------------------------------------------
# OUTPUT DATASET PATH
# -------------------------------------------------------

OUTPUT_DATA_PATH ="data/processed/encoded_customer_data.csv"

# -------------------------------------------------------
# LABEL ENCODERS PATH
# -------------------------------------------------------

ENCODERS_PATH = "models/label_encoders.pkl"

# =============================================================
# MAIN FUNCTION
# =============================================================

def main ():

    print("=" * 60)
    print(" CUSTOMER INTELLIGENCE DATA ENCODING ")
    print("=" * 60)

    # ---------------------------------------------------------
    # Create Object
    # ---------------------------------------------------------

    encoder = DataEncoder(INPUT_DATA_PATH)

    # ---------------------------------------------------------
    # Load Dataset
    # ---------------------------------------------------------

    print("\nLoading Cleaned Dataset...\n")

    encoder.load_data()


    # ---------------------------------------------------------
    # Encode Categorical Columns
    # ---------------------------------------------------------

    print("\nEncoding Categorical Columns...\n")

    encoder.encode_categorical_columns()

    # ---------------------------------------------------------
    # Save Label Encoders
    # ---------------------------------------------------------

    print("\nSaving Encoded Dataset...\n")

    encoder.save_encoders(ENCODERS_PATH)

    # ---------------------------------------------------------
    # Save Encoded Dataset
    # ---------------------------------------------------------

    print("\nSaving Encoded Dataset...\n")

    encoder.save_encoded_dataset(OUTPUT_DATA_PATH)

    print("\n" + "=" * 60)
    print("ENCODING COMPLETE SUCCESSFULLY")
    print("=" * 60)

    print("\nGenerated Files:")
    print(f"✔ {OUTPUT_DATA_PATH}")
    print(f"✔ {ENCODERS_PATH}")

    print("\nNext Step:")
    print("✔ Model Training")

# =============================================================
# PROGRAM STARTS HERE
# =============================================================

if __name__ == "__main__":
    main()