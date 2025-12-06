import os
from datetime import datetime

print("🚀 Starting Daily Automation...")

os.system("python ETL.py")
os.system("python FE.py")
os.system("python train_churn_model.py")
os.system("python daily_email.py")

print("🎯 All tasks completed successfully.")
with open("automation_log.txt", "a") as f:
    f.write("Automation ran successfully at: " + str(datetime.now()) + "\n")