import os

from pandas import read_csv

from interface.Server_Info_Collector import sdc_cli
from lfcomlib.Jessica import DaPr

DaPr = DaPr.Core()
Sdc_Cli = sdc_cli.SdcCli()


def merge(folder_or_name, output_file, show_msg=False, init_path=False, transpose_index_and_columns=False):
    if not init_path:
        dfs = load_data(folder_or_name, show_msg)
        merge_data(dfs, output_file, transpose_index_and_columns)
    else:
        report_folder, report_objs, report_objs_dev, report_objs_dev_objs = Sdc_Cli.init_merge_report_path(
            folder_or_name)
        output_file = report_objs_dev + '_merged_report.xlsx'
        print(report_objs_dev)
        dfs = []
        for folder in report_objs_dev_objs:
            report_objs_dev_sub = os.path.join(report_objs_dev, folder)
            if show_msg:
                print("report_objs_dev_sub", report_objs_dev_sub)
            print(report_objs_dev_sub)
            sub_dfs = load_data(report_objs_dev_sub, show_msg, check_file_name=['summary'])
            if sub_dfs is not None:
                dfs.extend(sub_dfs)
            print(sub_dfs)
        merge_data(dfs, output_file, transpose_index_and_columns)
        return report_folder, output_file


def load_data(report_folder, show_msg=False, check_file_name=None):
    dfs = []
    for obj in os.listdir(report_folder):
        if show_msg:
            print(obj)
        if os.path.splitext(obj)[-1] == '.csv' in obj:
            if check_file_name is not None:
                for x in check_file_name:
                    if x in obj:
                        dfs.append(csv_to_df(report_folder, obj))
            else:
                dfs.append(csv_to_df(report_folder, obj))
    return dfs


def csv_to_df(report_folder, obj, show_msg=False):
    csv_file = os.path.join(report_folder, obj)
    if show_msg:
        print(csv_file)
    csv_data = read_csv(csv_file, encoding='gb18030')
    if show_msg:
        print(csv_data)
    csv_data.set_index('item', inplace=True)
    return csv_data


def merge_data(dfs, output_file, transpose_index_and_columns=False):
    if len(dfs) != 0:
        final = dfs[0]
        for df in dfs[1:]:
            final = final.join(df, how='outer', lsuffix='item')
        if transpose_index_and_columns:
            final = final.T
        final.to_excel(output_file, engine='xlsxwriter')
    else:
        print("[!]No Data")
