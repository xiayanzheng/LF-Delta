import asyncio
import os
from common.data_hub import NdcHub
from handle_Network_Devices.flow import flow_async
from handle_Network_Devices.flow.flow_single import Dec
from handle_Network_Devices.flow import show_title
from handle_report import mergeReports
from interface.Network_Device_Check.ndc_cli import Cli
from lfcomlib.Jessica import DaPr
from lfcomlib.Jessica import Infra
from lfcomlib.Jessica.Log import log_time_spend
from lfcomlib.Jessica.Log import simple_err_log
Infra = Infra.Core()
DaPr = DaPr.Core()


class Interface(Cli):

    @log_time_spend()
    def flow(self):
        show_title.show()
        selected_group_name, config, config_report_root = self.load_config()
        async_config_queue, single_config_queue = self.repack_config(config)
        NdcHub.total_task_num = len(async_config_queue) + len(single_config_queue)
        self.set_report_folder_path(selected_group_name,config_report_root)
        self.run_async_task(async_config_queue)
        self.run_single_task(single_config_queue)
        print("[+]Data ready")
        self.merge_report_flow(NdcHub.report_folder_path)

    @staticmethod
    @simple_err_log()
    def run_async_task(config_queue):
        # print(config_queue)
        if len(config_queue) > 0:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(flow_async.run(config_queue))

    @staticmethod
    @simple_err_log()
    def run_single_task(config_queue):
        if len(config_queue) > 0:
            flow_single = Dec()
            flow_single.task(config_queue)

    @staticmethod
    def repack_config(cfg):
        async_support_devices = [
            "aruba_aos_6",
            "aruba_aos_8",
            "cisco_asa",
            "cisco_ios",
            "cisco_ios_xe",
            "cisco_ios_xr",
            "cisco_nxos",
            "fujitsu_switch",
            "hp_comware",
            "hp_comware_limited",
            "hw1000",
            "juniper_junos",
            "mikrotik_routeros",
            "terminal",
            "ubiquity_edge"
        ]
        single_config_queue = []
        async_config_queue = []
        for config_key, config in cfg.items():
            account = NdcHub.accounts[config['account']]
            config["config_name"] = config_key
            config["username"] = account["username"]
            config["password"] = account["password"]
            config["enablepass"] = account["enablepass"]
            if config["device_type"] in async_support_devices:
                async_config_queue.append(config)
                pass
            else:
                single_config_queue.append(config)
        return async_config_queue, single_config_queue

    @staticmethod
    @simple_err_log()
    def merge_report_flow(report_folder_path):
        print("[+]Merging reports")
        file_ext = '_merged_report.xlsx'
        output_file = os.path.join(report_folder_path, os.path.split(report_folder_path)[-1] + file_ext)
        mergeReports.merge(report_folder_path, output_file, transpose_index_and_columns=True)

