import os
import pandas as pd
from search import *
from collections import defaultdict


class AttributeDict(defaultdict):
    def __init__(self):
        super(AttributeDict, self).__init__(AttributeDict)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value


file_name = "run_code.xlsx"
xl_file = pd.ExcelFile(file_name)
dfs = xl_file.parse("Sheet1")
commandsToRun = dfs.loc[dfs['RUN_THIS_QUERY'] == 1, ['sno', 'animal', 'terms', 'dateFrom', 'dateTo',
                                                     'numOfSearchResults']]
for i in range(commandsToRun.__len__()):
    options = AttributeDict()
    for col, j in enumerate(commandsToRun.columns):
        options[j] = commandsToRun.iloc[i, col]
    print(f"Running search for Query {options['sno']}")
    runScript(options)


