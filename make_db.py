# make_db.py
# Parse the asl spreadsheets and create a relational database containing the same data

import sqlite3
import numpy as np
import pandas as pd

excel_file = 'master_list.xlsx'
asl_data = pd.read_excel(excel_file)
asl_data.replace({'(blank)': np.NaN, ' - PL':'',' - PAC':'', ' - PT':''}, inplace=True, regex=True)

db = sqlite3.connect(':memory:')
cur = db.cursor()

cur.execute('CREATE TABLE PF(id INTEGER PRIMARY KEY, name TEXT UNIQUE);')
cur.execute('CREATE TABLE PG(id INTEGER PRIMARY KEY, name TEXT UNIQUE, PFID INTEGER, \
                        FOREIGN KEY(PFID) REFERENCES PF(id));')
cur.execute('CREATE TABLE PL(id INTEGER PRIMARY KEY, name TEXT UNIQUE, PGID INTEGER, \
                        FOREIGN KEY(PGID) REFERENCES PG(id));')
cur.execute('CREATE TABLE PT(id INTEGER PRIMARY KEY, name TEXT UNIQUE, PLID INTEGER, \
                        FOREIGN KEY(PLID) REFERENCES PL(id));')

for row in asl_data.head(n=10).itertuples():
    if row.ProductFamily is not np.nan:
        cur.execute('INSERT OR IGNORE INTO PF (name) VALUES (?)', (row.ProductFamily,))
        cur.execute('INSERT OR IGNORE INTO PG (name, PFID) VALUES (?,?)', (row.ProductGroup, cur.lastrowid,))
        cur.execute('INSERT OR IGNORE INTO PL (name, PGID) VALUES (?,?)', (row.ProductLine, cur.lastrowid,))
        cur.execute('INSERT OR IGNORE INTO PT (name, PLID) VALUES (?,?)', (row.ProductType, cur.lastrowid,))

db.commit()

cur.execute('''
    SELECT 
        PF.name, PG.name, PL.name, PT.name 
    FROM 
        PF, PG, PL, PT
    WHERE
        PG.PFID = PF.ID AND
        PL.PGID = PG.ID AND
        PT.PLID = PL.ID
    LIMIT 20
''')

for row in cur.fetchall():
    print(row)



