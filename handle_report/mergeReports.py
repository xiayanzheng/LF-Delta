import os, prettytable
from pandas import read_csv
from lfcomlib.Jessica import DaPr

DaPr = DaPr.Core()


def init_path(group_name):
    report_root = DaPr.find_path_backward(os.getcwd(), 'Reports')
    report_objs = os.listdir(report_root)
    pt = prettytable.PrettyTable()
    pt.field_names = ['No', 'Report Name']
    repo_selections = {}
    count = 1
    for i in range(len(report_objs)):
        if group_name in report_objs[i]:
            index = str(count)
            repo_name = report_objs[i]
            print(">>", repo_name)
            if os.path.isdir(os.path.join(report_root, repo_name)):
                pt.add_row([index, repo_name])
                repo_selections[index] = repo_name
                count += 1
    print(pt)
    selected = input("Pls select a record：")
    if selected in list(repo_selections.keys()):
        report_objs_dev = os.path.join(report_root, repo_selections[selected])
        report_objs_dev_objs = os.listdir(report_objs_dev)
        return report_root, report_objs, report_objs_dev, report_objs_dev_objs
    else:
        print("Selected Group is not exists")
        init_path(group_name)


def merge(group_name, show_msg=False):
    # Load Report
    report_folder, report_objs, report_objs_dev, report_objs_dev_objs = init_path(group_name)
    output_file = report_objs_dev + '_merged_report.xlsx'
    dfs = load_data(report_folder, show_msg)
    merge_data(dfs, output_file)
    return report_folder, output_file


def merge_direct(report_folder, output_file, show_msg=False):
    dfs = load_data(report_folder, show_msg)
    merge_data(dfs, output_file)


def load_data(report_folder, show_msg=False):
    dfs = []
    for obj in os.listdir(report_folder):
        if show_msg:
            print(obj)
        if os.path.splitext(obj)[-1] == '.csv' in obj:
            csv_file = os.path.join(report_folder, obj)
            if show_msg:
                print(csv_file)
            csv_data = read_csv(csv_file, encoding='gb18030')
            if show_msg:
                print(csv_data)
            csv_data.set_index('item', inplace=True)
            dfs.append(csv_data)
    return dfs


def merge_data(dfs, output_file):
    if len(dfs) != 0:
        final = dfs[0]
        for df in dfs[1:]:
            final = final.join(df, how='outer', lsuffix='item')
        final.T.to_excel(output_file, engine='xlsxwriter')
    else:
        print("[!]No Data")
