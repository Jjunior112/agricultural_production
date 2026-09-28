import logging


from agricultural_production.bronze.extract_data import extract_data
from agricultural_production.silver.transform_data import transform_to_silver
from agricultural_production.gold.transform_data import transform_to_gold


logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    extract_data()
    transform_to_silver()
    transform_to_gold()
    
    