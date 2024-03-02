import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('Rogaland.db')
cursor = conn.cursor()

# Retrieve a list of all tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Generate and execute a DROP TABLE statement for each table
for table in tables:
    if table == "('sqlite_sequence',)":
        continue
    else:
        print(table)
    # drop_table_sql = f"DROP TABLE IF EXISTS {table[0]}"
    # cursor.execute(drop_table_sql)

# Commit changes and close the connection
conn.commit()
conn.close()
