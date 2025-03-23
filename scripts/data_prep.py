"""
Module 2: Initial Script to Verify Project Setup
File: scripts/data_prep.py
"""

import pandas as pd
from utils.logger import logger

# Constants and paths
import pathlib

PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"

def read_raw_data(file_name: str) -> pd.DataFrame:
    file_path = RAW_DATA_DIR / file_name
    try:
        logger.info(f"Reading raw data from {file_path}.")
        return pd.read_csv(file_path)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        return pd.DataFrame()

def process_data(file_name: str) -> None:
    df = read_raw_data(file_name)

def main() -> None:
    logger.info("Starting data preparation...")
    process_data("customers_data.csv")
    process_data("products_data.csv")
    process_data("sales_data.csv")
    logger.info("Data preparation complete.")

if __name__ == "__main__":
    main()
