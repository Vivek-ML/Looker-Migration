import os
import pandas as pd
import logging

# Enter the Dashboard name in Tableau
Tableau_Dashboard_Name = input("Enter the Dashboard name in Tableau:")
Looker_Dashboard_Name = input("Enter the Dashboard name in Looker:")

# Read CSV files with correct encoding and delimiter
file_path = f"C:\\Users\\User\\Downloads\\{Tableau_Dashboard_Name}.csv"
file_path1 = f"C:\\Users\\User\\Downloads\\{Looker_Dashboard_Name}.csv"



# Configure logging
logging.basicConfig(
    filename="file_comparison.log",  # Logs will be saved in this file
    level=logging.INFO,  # Change to DEBUG for more details
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Function to log messages
def log_message(level, message):
    print(message)  # Print to console
    if level == "info":
        logging.info(message)
    elif level == "warning":
        logging.warning(message)
    elif level == "error":
        logging.error(message)

# Try reading the Looker CSV file
try:
    if os.path.exists(file_path1):
        df1 = pd.read_csv(file_path)
        log_message("info", "✅ Looker CSV file read successfully!")
    else:
        log_message("error", f"❌ Error: The file '{file_path}' was not found.")
        df1 = None
except Exception as e:
    log_message("error", f"❌ Error reading the Looker file: {e}")
    df1 = None

# Try reading the Looker CSV file
try:
    if os.path.exists(file_path1):
        df2 = pd.read_csv(file_path1)  # Assuming it's a normal CSV
        print("✅ Looker CSV file read successfully!")
    else:
        print(f"❌ Error: The file '{file_path1}' was not found.")
        df2 = None
except Exception as e:
    print(f"❌ Error reading the Looker file: {e}")
    df2 = None

# Ensure both DataFrames are valid before proceeding
if df1 is not None and df2 is not None:
    # Normalize column names: Remove extra spaces, lowercase all
    df1.columns = df1.columns.str.strip().str.lower()
    df2.columns = df2.columns.str.strip().str.lower()

    # Check for missing columns in df2
    missing_columns = [col for col in df1.columns if col not in df2.columns]

    if missing_columns:
        log_message("warning", f"⚠️ Warning: Missing columns in Looker CSV: {', '.join(missing_columns)}")
        for col in missing_columns:
            df2[col] = None  # Add missing columns with NaN values

    # Ensure columns are in the same order
    df2 = df2[df1.columns]

    # Get number of rows
    rows_original = len(df1)
    rows_changed = len(df2)

    # Compare data safely
    try:
        differences = df1.compare(df2)
    except ValueError as e:
        log_message("warning", f"⚠️ Skipping comparison due to error: {e}")
        differences = pd.DataFrame()

    # Find missing rows
    missing_rows = df1[~df1.isin(df2)].dropna(how="all")

    # Calculate accuracy percentage
    matching_rows = rows_original - len(differences)
    accuracy = (matching_rows / rows_original) * 100 if rows_original else 0

    # Log Summary
    log_message("info", "🔍 File Comparison Summary:")
    log_message("info", f"📌 Total Rows in Tableau File: {rows_original}")
    log_message("info", f"📌 Total Rows in Looker File: {rows_changed}")
    log_message("info", f"📌 Accuracy Percentage: {accuracy:.2f}%")

    if not differences.empty:
        log_message("warning", f"🔹 Differences Found ({len(differences)} rows affected).")
        log_message("info", f"\n{differences}")
    else:
        log_message("info", "🏆 No differences found!")

    if not missing_rows.empty:
        log_message("warning", f"🔸 Missing Rows in Looker File ({len(missing_rows)} rows).")
        log_message("info", f"\n{missing_rows}")
    else:
        log_message("info", "🏆 No missing rows found!")

else:
    log_message("error", "❌ Skipping comparison due to missing files.")

