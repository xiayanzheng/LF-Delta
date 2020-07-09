import os

from handler.handle_report import mergeReports
from handler.handle_server.pipeline import common_process
from interface.Server_Info_Collector import sic_cli
from lfcomlib.Jessica import Infra

Infra = Infra.Core()
hscp = common_process.CommonProcess()


def main():
    # log_path, log_folder = set_path_and_select_group("SMBC")
    # get_server_data(log_path)
    Sdc_Cli = sic_cli.SicCli()
    group_name = Sdc_Cli.select_group()
    msg = "input [1] for get server status\ninput [2] for merge report\ninput [3] for reselect："
    selected_function = int(input(msg))
    if selected_function in [1, 2]:
        if selected_function == 1:
            log_path, log_folder = hscp.set_path_and_select_group(group_name)
            hscp.get_server_data(log_path)
            Infra.open_dir(log_path)
        elif selected_function == 2:
            output_path, output_file = mergeReports.merge(group_name, None, init_path=True)
            Infra.open_dir(output_path)
        elif selected_function == 3:
            main()
        os.system("pause")
    else:
        print("invalid input")
        main()
