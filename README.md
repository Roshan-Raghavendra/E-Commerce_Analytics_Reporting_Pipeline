# E-Commerce Analytics & Reporting Pipeline

A Python-based ETL project that ingests, cleans, transforms, consolidates, and loads synthetic e-commerce data into a SQLite database for SQL analysis.

## Pipeline

Excel workbook → Python/Pandas ETL → Cleaned CSV → SQLite database → SQL analysis

## Data

Place the workbook at `data/ecommerce_raw_data.xlsx`. It should contain `Orders`, `Customers`, and `Products` sheets. This is synthetic demonstration data, not real company data.

## ETL steps

1. Extract the three sheets with Pandas.
2. Validate required order columns.
3. Convert data types and handle missing values.
4. Remove duplicate order IDs.
5. Merge order, customer, and product data.
6. Calculate Gross Sales, Discount Amount, Net Sales, Total Cost, Profit, and Order Month.
7. Export the transformed dataset to CSV.
8. Load the result into the SQLite table `ecommerce_orders`.

## Run locally

```bash
pip install -r requirements.txt
python etl_pipeline.py
```

The pipeline writes `data/ecommerce_cleaned.csv` and `data/ecommerce.db`. SQL analysis examples are in `sql_queries.sql`.

## Validation

The project was previously tested: 553 raw order rows became 550 unique order IDs. The reporting dataset contains 21 columns, no remaining null values, and all six SQL analysis queries executed successfully against the generated SQLite database.

## Tech stack

Python, Pandas, SQL, SQLite, Excel

## Repository contents

- `etl_pipeline.py` — extraction, cleaning, transformation, and SQLite loading
- `sql_queries.sql` — six business analysis queries
- `requirements.txt` — Python dependencies
- `data/` — place the input workbook here before running the pipeline
