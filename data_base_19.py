import sqlite3
import pandas as pd

dtf19 = pd.read_csv('2019.csv')
conn = sqlite3.connect('nineteen.db')
conn.execute("DROP TABLE IF EXISTS nineteen_tbl")
dtf19.to_sql('nineteen_tbl', conn)
conn.close()
