import sqlite3
import pandas as pd

dtf18 = pd.read_csv('2018.csv')
conn = sqlite3.connect('eighteen.db')
conn.execute("DROP TABLE IF EXISTS eighteen_tbl")
dtf18.to_sql('eighteen_tbl', conn)
conn.close()
