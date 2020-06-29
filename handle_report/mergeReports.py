from init.init_imports import os, DaPrX, prettytable, read_csv
from init.init_imports import global_config as gc


def init_path(group_name):
    report_root = DaPrX.find_path_backward(os.getcwd(), 'Reports')
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
    report_root, report_objs, report_objs_dev, report_objs_dev_objs = init_path(group_name)
    dfs = []
    output_file = report_objs_dev + '_merged_report.xlsx'
    for folder in report_objs_dev_objs:
        report_objs_dev_sub = os.path.join(report_objs_dev, folder)
        if show_msg:
            print("report_objs_dev_sub", report_objs_dev_sub)
        for obj in os.listdir(report_objs_dev_sub):
            if show_msg:
                print(obj)
            if os.path.splitext(obj)[-1] == '.csv' and 'summary' in obj:
                csv_file = os.path.join(report_objs_dev_sub, obj)
                if show_msg:
                    print(csv_file)
                csv_data = read_csv(csv_file, encoding='gb18030')
                print(csv_data)
                csv_data.set_index('item', inplace=True)
                dfs.append(csv_data)
    if len(dfs) != 0:
        final = dfs[0]

        for df in dfs[1:]:
            temp = final.join(df, how='outer', lsuffix='item')
            final = temp
        final.to_excel(output_file, engine='xlsxwriter')
    else:
        print("No Data")
    return report_root, output_file


def merge_dirct(report_folder,show_msg=False):
    dfs = []
    output_file = os.path.join(report_folder,os.path.split(report_folder)[-1] + '_merged_report.xlsx')
    for obj in os.listdir(report_folder):
        print(obj)
        if show_msg:
            print(obj)
        if os.path.splitext(obj)[-1] == '.csv' in obj:
            csv_file = os.path.join(report_folder, obj)
            if show_msg:
                print(csv_file)
            csv_data = read_csv(csv_file, encoding='gb18030')
            print(csv_data)
            csv_data.set_index('item', inplace=True)
            dfs.append(csv_data)
    if len(dfs) != 0:
        final = dfs[0]
        for df in dfs[1:]:
            final = final.join(df, how='outer', lsuffix='item')
        final.to_excel(output_file, engine='xlsxwriter')
    else:
        print("No Data")