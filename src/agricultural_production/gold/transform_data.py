import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)


def transform_to_gold():
    
    project_root = Path(__file__).resolve().parents[3]

    silver_path = project_root / "data"/"silver"/"agricultural_production_silver.parquet"

    gold_path = project_root / "data" / "gold"

    logging.info(f"Reading Parquet from: {silver_path}")

    if not silver_path.exists():
        raise FileNotFoundError(f"Silver data file not found at: {silver_path}")

    df = pd.read_parquet(silver_path)
    
    logging.info(
        f"Silver records: {len(df)}"
    )
    
    # ==========================================================
    # Trata nulo da irrigação e fertilizante como não aplicado (somente esses nulos serão tratados na Silver)
    # ==========================================================
    
    df['irrigacao_mm'] = df['irrigacao_mm'].fillna(0)
    df['fertilizante_kg_ha'] = df['fertilizante_kg_ha'].fillna(0)
    
    # ==========================================================
    # Remove colunas de tch,atr e art para evitar data leakage
    # ==========================================================

    df = df.drop(['tch', 'atr', 'art'], axis=1)

    
    gold_path.mkdir(parents=True,exist_ok=True)

    output_path = gold_path / 'agricultural_production_gold.parquet'

    df.to_parquet(
        output_path,
        index=False
    )

    logging.info(
        f"Gold records: {len(df)}"
    )

    logging.info(
        f"Gold data saved to: {output_path}"
    )

    logging.info(
        "Silver → Gold transformation completed successfully."
    )

if __name__ == "__main__":
    transform_to_gold()