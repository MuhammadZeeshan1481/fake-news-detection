import sqlite3
import pandas as pd

db_path = "database/predictions.db"

conn = sqlite3.connect(db_path)
df = pd.read_sql_query("SELECT * FROM predictions", conn)
conn.close()

print(df)