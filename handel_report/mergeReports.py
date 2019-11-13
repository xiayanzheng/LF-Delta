from init.init_imports import os, DaPr, prettytable
import pandas as pd


def init_path(group_name):
    report_root = DaPr.find_path_backward(os.getcwd(), 'Reports')
    report_objs = os.listdir(report_root)
    pt = prettytable.PrettyTable()
    pt.field_names = ['No', 'Report Name']
    repo_dict = {}
    for i in range(len(report_objs)):
        if group_name in report_objs[i]:
            index = str(i)
            repo_name = report_objs[i]
            pt.add_row([index, repo_name])
            repo_dict[index] = repo_name
    print(pt)
    selected = input("Pls select a record：")
    if selected in list(repo_dict.keys()):
        report_objs_dev = os.path.join(report_root, repo_dict[selected])
        report_objs_dev_objs = os.listdir(report_objs_dev)
        return report_root, report_objs, report_objs_dev, report_objs_dev_objs
    else:
        print("Selected Group is not exists")
        init_path(group_name)


def merge(group_name):
    # Load Report
    report_root, report_objs, report_objs_dev, report_objs_dev_objs = init_path(group_name)
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
    for df in dfs[1:]:
        temp = final.join(df, how='outer', lsuffix='item')
        final = temp
    final.to_excel("merged_report.xlsx", engine='xlsxwriter')

