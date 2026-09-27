import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)


def transform_to_silver():
    
    project_root = Path(__file__).resolve().parents[3]

    bronze_path = project_root / "data"/"bronze"/"agricultural_production.parquet"

    silver_path = project_root / "data" / "silver"

    logging.info(f"Reading Parquet from: {bronze_path}")

    if not bronze_path.exists():
        raise FileNotFoundError(f"Bronze data file not found at: {bronze_path}")

    df = pd.read_parquet(bronze_path)
    
    logging.info(
        f"Bronze records: {len(df)}"
    )
    
    # ==========================================================
    # Padro nomes de estados e municipios
    # ==========================================================
    
    df['estado'] = df['estado'].str.title()

    df['municipio'] = df['municipio'].str.title()

    # ==========================================================
    # Padroniza nome da cultura removendo espaços
    # ==========================================================

    df['cultura'] = df['cultura'].str.strip()    

    # ==========================================================
    # Trata nulo da irrigação e fertilizante como não aplicado (somente esses nulos serão tratados na Silver)
    # ==========================================================
    
    df['irrigacao_mm'] = df['irrigacao_mm'].fillna(0)
    df['fertilizante_kg_ha'] = df['fertilizante_kg_ha'].fillna(0)
    
    # ==========================================================
    # Remove colunas de tch,atr e art para evitar data leakage
    # ==========================================================

    df = df.drop(['tch', 'atr', 'art'], axis=1)

    
    silver_path.mkdir(parents=True,exist_ok=True)

    output_path = silver_path / 'agricultural_production_silver.parquet'

    df.to_parquet(
        output_path,
        index=False
    )

    logging.info(
        f"Silver records: {len(df)}"
    )

    logging.info(
        f"Silver data saved to: {output_path}"
    )

    logging.info(
        "Bronze → Silver transformation completed successfully."
    )


#if __name__ == "__main__":
transform_to_silver()