"""
Run this script ONCE locally to convert slow .xls files → fast .csv files.
This dramatically speeds up the Streamlit app (10-50x faster data loading).

Usage:
    python convert_data.py
"""
import pandas as pd
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

XLS_TO_CSV = [
    ("20260106153152255_Admission 2023 24.xls", "admission_2023_24.csv"),
    ("20260106153439552_Admission 2024 25.xls", "admission_2024_25.csv"),
    ("20260106153808096_Admission 2025 26.xls", "admission_2025_26.csv"),
    ("20260106153841088_Admission 2026 27.xls", "admission_2026_27.csv"),
]

print("=" * 50)
print("Converting .xls files to .csv for faster loading")
print("=" * 50)

for xls_name, csv_name in XLS_TO_CSV:
    xls_path = os.path.join(BASE_DIR, xls_name)
    csv_path = os.path.join(DATA_DIR, csv_name)

    if not os.path.exists(xls_path):
        print(f"  SKIP  {xls_name} (not found)")
        continue

    print(f"  Converting {xls_name}...", end=" ", flush=True)
    t0 = time.time()
    df = pd.read_excel(xls_path, header=3, engine="xlrd")
    df.to_csv(csv_path, index=False)
    elapsed = time.time() - t0
    print(f"OK  ({len(df):,} rows, {elapsed:.1f}s)")

print("\nDone! CSV files saved to data/ folder.")
print("You can now commit the data/ folder to Git.")
print("The Streamlit app will automatically use CSV files for faster loading.")
