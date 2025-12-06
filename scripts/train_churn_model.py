# ============================================================
# FILE: train_churn_model.py
# PURPOSE: Train churn prediction model and store predictions
# AUTHOR: Anuj Upadhyay (Elite Data Analyst Project)
# ============================================================

import pyodbc
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

# ------------------------------------------------------------
# 1️⃣ CONNECT TO SQL SERVER
# ------------------------------------------------------------
try:
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=ANUJ_LAPTOP;'
        'DATABASE=AUTOMAION;'
        'Trusted_Connection=yes;'
    )
    print("✅ Connected to SQL Server successfully.")
except Exception as e:
    print("❌ SQL Connection failed:", e)
    exit()

# ------------------------------------------------------------
# 2️⃣ FETCH CUSTOMER FEATURES
# ------------------------------------------------------------
query = "SELECT * FROM vw_customer_features"
df = pd.read_sql(query, conn)
conn.close()
print(f"✅ Data fetched: {df.shape[0]} rows, {df.shape[1]} columns")

# ------------------------------------------------------------
# 3️⃣ DATA PREPARATION
# ------------------------------------------------------------

# Remove rows with missing or invalid data
df = df.dropna()

# Feature selection
feature_cols = [
    'total_tickets',
    'avg_response_hours',
    'days_since_last_purchase',
    'total_purchases',
    'total_revenue',
    'avg_order_value',
    'avg_response_time',
    'stress_index'  # if available in your SQL view
]

# Keep only existing columns
X = df[[c for c in feature_cols if c in df.columns]]
y = df['likely_churn_flag']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ------------------------------------------------------------
# 4️⃣ TRAIN MODEL
# ------------------------------------------------------------
model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)

# ------------------------------------------------------------
# 5️⃣ EVALUATE MODEL
# ------------------------------------------------------------
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"🎯 Model Accuracy: {accuracy:.2%}")
print(classification_report(y_test, y_pred))

# ------------------------------------------------------------
# 6️⃣ SAVE MODEL + SCALER
# ------------------------------------------------------------
joblib.dump(model, "churn_model.pkl")
joblib.dump(scaler, "scaler.pkl")
print("💾 Model and scaler saved successfully.")

# ------------------------------------------------------------
# 7️⃣ PREDICT ON FULL DATASET
# ------------------------------------------------------------
X_scaled = scaler.transform(X)
df['churn_probability'] = model.predict_proba(X_scaled)[:, 1]

# ------------------------------------------------------------
# 8️⃣ WRITE RESULTS BACK TO SQL
# ------------------------------------------------------------
try:
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=ANUJ_LAPTOP;'
        'DATABASE=AUTOMAION;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
    IF OBJECT_ID('Customer_Churn_Predictions', 'U') IS NULL
    BEGIN
        CREATE TABLE Customer_Churn_Predictions (
            id INT IDENTITY(1,1) PRIMARY KEY,
            customer_id INT,
            churn_probability FLOAT,
            predicted_date DATETIME DEFAULT GETDATE()
        )
    END
    """)
    conn.commit()

    # Clear old records (optional, to avoid duplicates)
    cursor.execute("DELETE FROM Customer_Churn_Predictions")
    conn.commit()

    # Insert new predictions
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO Customer_Churn_Predictions (customer_id, churn_probability)
            VALUES (?, ?)
        """, int(row.customer_id), float(row.churn_probability))
    conn.commit()

    print(f"✅ {len(df)} predictions written to SQL Server successfully.")
    conn.close()

except Exception as e:
    print("❌ Error writing predictions to SQL Server:", e)

print("🏁 Churn model training and prediction complete.")
