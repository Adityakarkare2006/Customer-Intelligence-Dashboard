import utils.preprocess

print(utils.preprocess.__file__)

from utils.preprocess import DataPreprocessor

processor = DataPreprocessor("data/raw/customer_churn.csv")

processor.load_data()

processor.dataset_info()

processor.check_missing_values()

processor.check_duplicates()

processor.load_data()

processor.dataset_info()

processor.check_missing_values()

processor.handle_missing_values()

processor.check_duplicates()

processor.remove_duplicates_()

processor.clean_text_columns()

processor.save_cleaned_data(
    "data/processed/cleaned_customer_data.csv"
)