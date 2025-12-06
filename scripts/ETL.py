import pandas as pd
import pyodbc
import os

# SQL Server connection details
SERVER = "ANUJ_LAPTOP"
DATABASE = "AUTOMAION"

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
    "Encrypt=no;"
)

# Create SQL connection
cnxn = pyodbc.connect(connection_string)
cursor = cnxn.cursor()

def load_data(csv_file, table_name):
    """Loads a CSV file into SQL Server table."""
    df = pd.read_csv(csv_file)

    # Insert row-by-row
    for index, row in df.iterrows():
        columns = ", ".join(df.columns)
        placeholders = ", ".join(["?"] * len(df.columns))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(row))

    cnxn.commit()
    print(f"✅ Loaded {csv_file} → {table_name} ({len(df)} rows)")


# Load all files
load_data("data/customers.csv", "customers")
load_data("data/products.csv", "products")
load_data("data/sales_data.csv", "sales_data")
load_data("data/support_tickets.csv", "support_tickets")

print("🎯 All data successfully loaded into SQL Server!")
# Close the connection