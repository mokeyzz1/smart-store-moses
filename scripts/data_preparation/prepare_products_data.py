"""
scripts/data_preparation/prepare_products_data.py

This script reads product data from the data/raw folder, cleans it using the reusable DataScrubber class,
and writes the cleaned version to the data/prepared folder.

To Run:
$ source .venv/bin/activate
$ python scripts/data_preparation/prepare_products_data.py
"""

import pathlib
import sys
import pandas as pd
from loguru import logger

# Add project root to sys.path for local imports
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Import reusable class
from scripts.data_scrubber import DataScrubber  # noqa: E402

# Constants
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PREPARED_DATA_DIR = DATA_DIR / "prepared"

def read_raw_data(file_name: str) -> pd.DataFrame:
    file_path = RAW_DATA_DIR / file_name
    logger.info(f"Reading data from {file_path}")
    return pd.read_csv(file_path)

def save_prepared_data(df: pd.DataFrame, file_name: str) -> None:
    PREPARED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    file_path = PREPARED_DATA_DIR / file_name
    df.to_csv(file_path, index=False)
    logger.info(f"Saved cleaned data to {file_path}")

def main() -> None:
    logger.info("==================================")
    logger.info("STARTING prepare_products_data.py")
    logger.info("==================================")

    input_file = "products_data.csv"
    output_file = "products_data_prepared.csv"

    df = read_raw_data(input_file)
    logger.info(f"Initial dataframe shape: {df.shape}")
    logger.info(f"Initial columns: {list(df.columns)}")

    # Initialize scrubber
    scrubber = DataScrubber(df)

    # Check data before cleaning
    logger.info("Data consistency before cleaning:")
    logger.info(scrubber.check_data_consistency_before_cleaning())

    # Clean column names
    scrubber.df.columns = scrubber.df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Apply cleaning steps
    scrubber.remove_duplicate_records()
    scrubber.handle_missing_data(fill_value=0)
    scrubber.filter_column_outliers("stockquantity", 0, 5000)
    scrubber.format_column_strings_to_lower_and_trim("subcategory")

    # Final validation
    logger.info("Data consistency after cleaning:")
    logger.info(scrubber.check_data_consistency_after_cleaning())

    # Save result
    save_prepared_data(scrubber.df, output_file)

    logger.info("==================================")
    logger.info("FINISHED prepare_products_data.py")
    logger.info("==================================")

if __name__ == "__main__":
    main()
