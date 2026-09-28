import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)


def extract_data():
    project_root = Path(__file__).resolve().parents[3]

    raw_data = project_root / "sample"/"agricultural_production_raw.csv"
    
    storage_path = project_root / "data" / "bronze"

    logging.info(f"Reading CSV from: {raw_data}")

    if not raw_data.exists():
        raise FileNotFoundError(f"Raw data file not found at: {raw_data}")
    
    df = pd.read_csv(raw_data,delimiter=";", dtype={'id_registro':str})

    storage_path.mkdir(parents=True, exist_ok=True)

    output_path = storage_path / 'agricultural_production.parquet'

    df.to_parquet(
        output_path,
        index=False
    )
    
    logging.info(f"Raw data saved to: {output_path}")
    logging.info(f"Records processed: {len(df)}")
    logging.info(f"Columns processed: {len(df.columns)}")



if __name__ == "__main__":
    extract_data()