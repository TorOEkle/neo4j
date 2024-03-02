import csv
import sqlite3
from pathlib import Path

db_path = Path('Rogaland.db')
csv_path = Path("csv")

csv_files = {
    csv_path/'persons.csv': 'Persons',
    csv_path/'families.csv': 'Families',
    csv_path/'households.csv': 'Households',
    csv_path/'household_members.csv': 'HouseholdMembers',
    csv_path/'csvparent_child.csv': 'ParentChild',
}

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def load_csv_into_table(csv_file_path, table_name):
    with open(csv_file_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        columns = ', '.join(reader.fieldnames)
        placeholders = ', '.join(['?'] * len(reader.fieldnames))
        sql = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
        
        for row in reader:
            cursor.execute(sql, list(row.values()))


for csv_file, table_name in csv_files.items():
    csv_path = Path(csv_file)
    if csv_path.exists():
        print(f"Loading data from {csv_file} into {table_name}")
        load_csv_into_table(csv_path, table_name)
    else:
        print(f"File {csv_file} not found. Skipping...")

conn.commit()
conn.close()

print("Data import complete.")
