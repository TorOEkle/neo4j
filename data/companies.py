from pathlib import Path
import pandas as pd

csvPath = Path("data")/ Path("csv_files")

companies = pd.read_csv(csvPath/"enheter.csv")

print(companies.head(10))