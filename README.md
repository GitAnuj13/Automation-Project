📊 Automated Customer Support Intelligence System

A complete end-to-end analytics automation pipeline using Python, SQL Server, Machine Learning, and Power BI.

🚀 Overview

This project builds a production-style automated analytics system that processes customer support data daily, generates KPIs, trains a churn prediction model, sends automated email reports, and refreshes a Power BI dashboard — fully hands-off.

The goal is to simulate a real Analytics Engineering + Machine Learning Automation workflow.

🏗️ System Architecture
1️⃣ Data → SQL Server (ETL Pipeline)

Python scripts load and clean data from CSV files into SQL Server using pyodbc.
Feature engineering is applied to support tickets and customer behavior.

2️⃣ Daily KPI Engine

A Python script calculates operational KPIs such as:

Average response time

SLA compliance

Fast ticket ratio

Weekend ticket share

Results are stored in daily_kpi_summary table.

3️⃣ Machine Learning (Churn Prediction)

A scikit-learn model predicts churn probability using engineered features.
Predictions are saved back to SQL in Customer_Churn_Predictions.

4️⃣ Email Automation

A Python email bot generates HTML reports containing:

Daily KPIs

Top at-risk customers

Churn insights

Automatically delivered every morning.

5️⃣ Power BI Dashboard (Automated Refresh)

Power BI connects to SQL Server via Gateway, enabling daily scheduled refresh.
Dashboard includes:

Churn probability visuals

Risk segmentation

KPI trends

Customer drill-through view

6️⃣ Task Scheduler Orchestration

A master script daily_run.py orchestrates the entire pipeline:
ETL → KPI → ML → Predictions → Email → Refresh.
Windows Task Scheduler triggers this every morning.

🧱 Folder Structure
Automation-Project/
│
├── data/                  # Raw CSV files (not uploaded for privacy)
│
├── scripts/               # All Python modules
│   ├── load_to_sql.py
│   ├── daily_kpi_summary.py
│   ├── train_churn_model.py
│   ├── generate_predictions.py
│   ├── email_report.py
│   └── clean_support_tickets.py
│
├── automation/
│   ├── daily_run.py       # Master automation script
│   └── automation_log.txt # Log outputs
│
├── sql/
│   ├── create_tables.sql
│   ├── views.sql
│   └── churn_features.sql
│
├── powerbi/
│   ├── churn_theme.json
│   └── dashboard_layout_notes.txt
│
├── README.md
├── .gitignore
└── requirements.txt

💡 Technologies Used
Python

pandas

pyodbc

scikit-learn

joblib

smtplib / email.mime

os (automation)

datetime

SQL Server

Data warehousing

Feature engineering views

KPI summary table

Churn prediction storage

Power BI

Dashboard for churn insights

SQL Gateway

Scheduled refresh

Automation Framework

daily_run.py as orchestrator

Windows Task Scheduler for cron-style execution

🔍 Key Features

✔ Automated ETL → SQL
✔ KPI Engine
✔ ML model training & prediction
✔ Predictions written to SQL
✔ Automated HTML email report
✔ Power BI dashboard auto-refresh
✔ Pipeline logs for monitoring
✔ Modularized script structure

🖼️ Power BI Dashboard Highlights

Churn probability distribution

High-risk customer list

SLA trends

Response time vs churn

Region-level churn heatmaps

Customer drill-through page

▶️ How to Run the Pipeline



Run the master script manually:

python automation/daily_run.py


Set up Windows Task Scheduler to run daily.

📬 Future Enhancements

Add anomaly detection on support metrics

API-based data ingestion

Dockerized deployment

Airflow or Prefect orchestration upgrade

🙌 Author

Anuj Upadhyay
Data Analyst • Analytics Engineering • Automation & ML Projects
