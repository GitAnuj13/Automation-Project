import pyodbc
import pandas as pd
from datetime import datetime

# -----------------------------
# SQL CONNECTION
# -----------------------------
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=ANUJ_LAPTOP;'
    'DATABASE=AUTOMAION;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

print("🔗 Connected to SQL Server")

# -----------------------------
# STEP 1: Fetch raw data
# -----------------------------
query = """
SELECT customer_id, ticket_date, response_hours
FROM support_tickets
"""
df = pd.read_sql_query(query, conn)

# -----------------------------
# STEP 2: Data cleaning
# -----------------------------
df.dropna(subset=['customer_id', 'response_hours'], inplace=True)
df['ticket_date'] = pd.to_datetime(df['ticket_date'])

# -----------------------------
# STEP 3: Feature engineering
# -----------------------------
df['ticket_week'] = df['ticket_date'].dt.isocalendar().week.astype(int)
df['ticket_month'] = df['ticket_date'].dt.month
df['is_weekend'] = (df['ticket_date'].dt.dayofweek >= 5).astype(int)

df['response_speed_category'] = pd.cut(
    df['response_hours'],
    bins=[0, 4, 12, 1000],
    labels=['Fast', 'Medium', 'Slow']
).astype(str)

df['sla_met'] = (df['response_hours'] <= 8).astype(int)

# -----------------------------
# STEP 4: Create staging table
# -----------------------------

cursor.execute("""
IF OBJECT_ID('stg_support_tickets', 'U') IS NOT NULL 
    DROP TABLE stg_support_tickets;
""")
conn.commit()

cursor.execute("""
CREATE TABLE stg_support_tickets (
    customer_id INT,
    ticket_date DATETIME,
    response_hours FLOAT,
    ticket_week INT,
    ticket_month INT,
    is_weekend BIT,
    response_speed_category NVARCHAR(20),
    sla_met BIT
);
""")
conn.commit()

# -----------------------------
# STEP 5: Insert cleaned data
# -----------------------------
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO stg_support_tickets 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, 
        row.customer_id, 
        row.ticket_date, 
        row.response_hours, 
        int(row.ticket_week),
        row.ticket_month, 
        row.is_weekend, 
        row.response_speed_category, 
        row.sla_met
    )

conn.commit()

print("✅ Data cleaning & feature engineering complete.")
conn.close()
