from init.init_imports import Infra, os, DaPr
import csv, pandas
import pandas as pd
from openpyxl import load_workbook
from xlutils.copy import copy as xl_copy

# Load Report
report_root = DaPr.find_path_backward(os.getcwd(), 'Reports')
report_objs = os.listdir(report_root)
report_objs_dev = os.path.join(report_root, report_objs[0])
report_objs_dev_objs = os.listdir(report_objs_dev)
merged = pd.ExcelWriter(os.path.join(report_objs_dev, "merged.xlsx"))
dfs = []

for x in report_objs_dev_objs:
    report_objs_dev_sub = os.path.join(report_objs_dev, x)
    for obj in os.listdir(report_objs_dev_sub):
        if os.path.splitext(obj)[-1] == '.csv' and "Summary" in obj:
            csv_file = os.path.join(report_objs_dev_sub, obj)
            csv_data = pd.read_csv(csv_file)
            csv_data.set_index('item', inplace=True)
            dfs.append(csv_data)

final = dfs[0]
print(type(final))
for df in dfs[1:]:
    print(type(df))
    temp = final.join(df, how='outer', lsuffix='item')
    final = temp
print(final)
final.to_excel("mgs.xlsx", engine='xlsxwriter')
