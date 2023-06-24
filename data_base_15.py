import sqlite3
import pandas as pd

dtf15 = pd.read_csv('2015.csv')
conn = sqlite3.connect('fifteen.db')
conn.execute("DROP TABLE IF EXISTS fifteen_tbl")
dtf15.to_sql('fifteen_tbl', conn)
conn.close()
