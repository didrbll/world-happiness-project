import sqlite3
import pandas as pd

dtf17 = pd.read_csv('2017.csv')
conn = sqlite3.connect('seventeen.db')
conn.execute("DROP TABLE IF EXISTS seventeen_tbl")
dtf17.to_sql('seventeen_tbl', conn)
conn.close()