# ETL Process for Food Recall Data

This folder contains the ETL (Extract, Transform, Load) process for handling food recall data. The process involves downloading data, cleaning it, and preparing it for analysis.

## Files

- `1_generate_db.py`: This script downloads the recall data and the Open Food Facts data, processes it, and merges the datasets.
- `2_clean_db.py`: This script cleans the merged data, extracts relevant information, and prepares it for analysis.

## Steps

### 1. Generate Database

The `1_generate_db.py` script performs the following steps:
1. Downloads the recall data from the provided URL.
2. Saves the recall data as a JSON file in the `etl/input` folder.
3. Reads the Open Food Facts data from a CSV file.
4. Processes the GTIN (Global Trade Item Number) to ensure it is valid and properly formatted.
5. Merges the recall data with the Open Food Facts data.
6. Saves the processed data to a CSV file in the `etl/output` folder.

### 2. Clean Database

The `2_clean_db.py` script performs the following steps:
1. Loads the processed data from the `etl/output` folder.
2. Extracts the department information from the `zone_geographique_de_vente` column.
3. Cleans and processes the department information.
4. Merges the data with geographical information from a GeoJSON file.
5. Classifies the risks associated with the recalls.
6. Saves the cleaned data to CSV and JSONL files in the `etl/output` folder.

## Usage

To run the ETL process, execute the following commands:

```sh
python etl/1_generate_db.py
python etl/2_clean_db.py