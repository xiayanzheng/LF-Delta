from init.init_imports import Infra, os, DaPr
import csv, pandas
import pandas as pd
from openpyxl import load_workbook
from xlutils.copy import copy as xl_copy

# Load Report
report_root = DaPr.find_path_backward(os.getcwd(), 'Reports')
report_objs = os.listdir(report_root)
report_obj_dev = os.path.join(report_root, report_objs[0])
report_obj_dev_objs = os.listdir(report_obj_dev)




os.system("explorer %s" % os.getcwd())
