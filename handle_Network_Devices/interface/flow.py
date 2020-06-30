from lfcomlib.Jessica import DaPr
from lfcomlib.Jessica import Infra
from handle_report import mergeReports
from handle_Network_Devices.interface import show_title
import prettytable
import os
import asyncio
import time
from handle_Network_Devices.interface.pipline import DeviceCheck

Infra = Infra.Core()
DaPr = DaPr.Core()
dc = DeviceCheck()


class Interface:

    def __init__(self):
        self.wait_task_num = 0
        self.total_task_num = 0

    def flow(self):
        start = time.time()
        show_title.show()
        device_info = self.load_config()
        loop = asyncio.get_event_loop()
        tasks = []
        self.total_task_num, self.wait_task_num = len(device_info), len(device_info)
        for device_name, cfg in device_info.items():
            task = self.execute(device_name, cfg)
            tasks.append(task)
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
        file_ext = '_merged_report.xlsx'
        output_file = os.path.join(dc.report_folder_path, os.path.split(dc.report_folder_path)[-1] + file_ext)
        mergeReports.merge_direct(dc.report_folder_path, output_file)
        end = time.time()
        input("[+]Done.Total process time used: {} seconds".format(int(end-start)))

    async def execute(self, device_name, cfg):
        # for device_name, cfg in device_info.items():
        self.wait_task_num -= 1
        self.show_progress()
        account = dc.accounts[cfg["account"]]
        cfg["ip"] = cfg['host']
        cfg["device_name"] = device_name
        cfg["username"] = account['username']
        cfg["password"] = account['password']
        cfg["enablepass"] = account['enablepass']
        dc.get_info(**cfg)

    def show_progress(self):
        total = self.total_task_num
        wait = self.wait_task_num
        print("[+]Task status:Total {},Wait {}".format(total,wait))


    def load_config(self):
        config_file_path = DaPr.find_path_backward(os.getcwd(), 'config')
        cfg = Infra.read_yaml(config_file_path, 'network_device_config.yaml')
        dc.commands = cfg["commands"]
        dc.tasks = cfg["tasks"]
        dc.groups = cfg["groups"]
        dc.accounts = cfg["accounts"]
        dc.regx_rules = cfg["regx_rules"]
        selected_group = self.select_group(dc.groups)
        return selected_group

    def select_group(self, groups):
        group_list = []
        for k, v in groups.items():
            group_list.append(k)
        pt = prettytable.PrettyTable()
        pt.field_names = ["ID", "Group"]
        for i in range(len(group_list)):
            no = i
            group = group_list[i]
            pt.add_row([no, group])
        print(pt)
        selected = int(input("[>]Pls select a group by ID："))
        return groups[group_list[selected]]
