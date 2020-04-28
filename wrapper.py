import os
import pandas as pd

file_name = "run_code.xlsx"
xl_file = pd.ExcelFile(file_name)
dfs = xl_file.parse("Sheet1")
commandsToRun = dfs.loc[dfs['RUN_THIS_QUERY'] == 1, ['code', 'sno']]

for i in commandsToRun.values:
    print(f"Running search for Query {i[1]}")
    os.system(i[0])

