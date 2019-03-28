# make_db.py
# Parse the asl spreadsheets and create a relational database containing the same data

import sqlite3
import numpy as np
import pandas as pd

excel_file = 'master_list.xlsx'

asl_data = pd.read_excel(excel_file)

asl_data.replace({'(blank)': np.NaN, ' - PL':'',' - PAC':'', ' - PT':''}, inplace=True, regex=True)

print(asl_data[['ProductType','ProductLine','ProductGroup','ProductFamily']].head())


