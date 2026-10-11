import pandas as pd
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_FILE = DATA_DIR / "ecommerce_raw_data.xlsx"
CLEAN_FILE = DATA_DIR / "ecommerce_cleaned.csv"
DB_FILE = DATA_DIR / "ecommerce.db"


def run_etl():
    # Extract
    orders = pd.read_excel(RAW_FILE, sheet_name="Orders")
    customers = pd.read_excel(RAW_FILE, sheet_name="Customers")
    products = pd.read_excel(RAW_FILE, sheet_name="Products")

    print(f"Raw orders: {len(orders)}")

    # Validate required columns
    required_orders = {
        "Order_ID", "Order_Date", "Customer_ID", "Product_ID",
        "Quantity", "Discount", "Payment_Method", "Order_Status"
    }
    missing_columns = required_orders - set(orders.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    # Clean orders
    orders["Order_Date"] = pd.to_datetime(orders["Order_Date"], errors="coerce")
    orders["Quantity"] = pd.to_numeric(orders["Quantity"], errors="coerce")
    orders["Discount"] = pd.to_numeric(orders["Discount"], errors="coerce")

    orders["Quantity"] = orders["Quantity"].fillna(1)
    orders["Discount"] = orders["Discount"].fillna(0)
    orders["Payment_Method"] = orders["Payment_Method"].fillna("Unknown")
    orders["Order_Status"] = orders["Order_Status"].fillna("Unknown")
    orders["Customer_ID"] = orders["Customer_ID"].fillna("Unknown")

    # Remove duplicate order IDs
    orders = orders.drop_duplicates(subset=["Order_ID"], keep="first")

    # Consolidate order + customer + product information
    final = (
        orders
        .merge(customers, on="Customer_ID", how="left")
        .merge(products, on="Product_ID", how="left")
    )

    # Handle unmatched lookup values
    for col in ["Customer_Name", "City", "Customer_Segment"]:
        if col in final.columns:
            final[col] = final[col].fillna("Unknown")

    # Feature transformations
    final["Gross_Sales"] = final["Quantity"] * final["Unit_Price"]
    final["Discount_Amount"] = final["Gross_Sales"] * final["Discount"]
    final["Net_Sales"] = final["Gross_Sales"] - final["Discount_Amount"]
    final["Total_Cost"] = final["Quantity"] * final["Unit_Cost"]
    final["Profit"] = final["Net_Sales"] - final["Total_Cost"]
    final["Order_Month"] = final["Order_Date"].dt.to_period("M").astype(str)

    columns = [
        "Order_ID", "Order_Date", "Order_Month", "Customer_ID", "Customer_Name",
        "City", "Customer_Segment", "Product_ID", "Product_Name", "Category",
        "Quantity", "Unit_Price", "Discount", "Gross_Sales", "Discount_Amount",
        "Net_Sales", "Unit_Cost", "Total_Cost", "Profit", "Payment_Method", "Order_Status"
    ]
    final = final[columns].sort_values("Order_Date")

    final.to_csv(CLEAN_FILE, index=False)

    with sqlite3.connect(DB_FILE) as conn:
        final.to_sql("ecommerce_orders", conn, if_exists="replace", index=False)

    print(f"Cleaned records: {len(final)}")
    print(f"Saved cleaned data to: {CLEAN_FILE}")
    print("Loaded data into SQL table: ecommerce_orders")
    print(f"SQLite database: {DB_FILE}")


if __name__ == "__main__":
    run_etl()
