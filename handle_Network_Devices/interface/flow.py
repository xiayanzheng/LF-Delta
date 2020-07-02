from lfcomlib.Jessica import DaPr
from lfcomlib.Jessica import Infra
from handle_report import mergeReports
from handle_Network_Devices.interface import show_title
import prettytable
import os
import asyncio
import time
from handle_Network_Devices.interface.pipline import DeviceCheck
from interface.Network_Device_Check.ndc_cli import Cli
from common.data_hub import NdcHub
from handle_Network_Devices.interface import async_flow
Infra = Infra.Core()
DaPr = DaPr.Core()
dc = DeviceCheck()


class Interface(Cli):

    def __init__(self):
        self.wait_task_num = 0
        self.total_task_num = 0

    def flow(self):
        start = time.time()
        show_title.show()
        config = self.load_config()
        devices = self.repack_config(config)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(async_flow.run(devices))
        file_ext = '_merged_report.xlsx'
        try:
            output_file = os.path.join(dc.report_folder_path, os.path.split(dc.report_folder_path)[-1] + file_ext)
            mergeReports.merge_direct(dc.report_folder_path, output_file,transpose_index_and_columns=True)
        except Exception as e:
            print("[!]Err-Msg:{}".format(e))
        end = time.time()
        input("[+]Done.Total process time used: {} seconds".format(int(end-start)))

    def repack_config(self, cfg):
        config_queue = []
        for config_key,config in cfg.items():
            account = NdcHub.accounts[config['account']]
            config["config_name"] = config_key
            config["username"] = account["username"]
            config["password"] = account["password"]
            config["enablepass"] = account["enablepass"]
            config_queue.append(config)
        return config_queue
