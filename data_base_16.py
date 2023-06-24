import sqlite3
import pandas as pd

dtf16 = pd.read_csv('2016.csv')
conn = sqlite3.connect('sixteen.db')
conn.execute("DROP TABLE IF EXISTS sixteen_tbl")
dtf16.to_sql('sixteen_tbl', conn)
conn.close()
