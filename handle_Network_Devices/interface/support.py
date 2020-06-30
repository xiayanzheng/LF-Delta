from lfcomlib.Jessica import DaPr
from lfcomlib.Jessica import Infra
from handle_report import mergeReports
from handle_Network_Devices.interface import show_title
import prettytable
import os
import asyncio
import time
from handle_Network_Devices.interface.pipline import DeviceCheck
from handle_Network_Devices.cisco import connector_async
Infra = Infra.Core()
DaPr = DaPr.Core()
dc = DeviceCheck()
hc = connector_async.Connection()

class SupportFunc:

    # def show_progress(self):
    #     total = self.total_task_num
    # wait = self.wait_task_num
    # print("[+]Task status:Total {},Wait {}".format(total,wait))

    def load_config(self):
        config_file_path = DaPr.find_path_backward(os.getcwd(), 'config')
        cfg = Infra.read_yaml(config_file_path, 'network_device_config.yaml')
        dc.commands = cfg["commands"]
        dc.tasks = cfg["tasks"]
        print("tasks",dc.tasks)
        dc.groups = cfg["groups"]
        dc.accounts = cfg["accounts"]
        dc.regx_rules = cfg["regx_rules"]
        selected_group = self.select_group(dc.groups)
        return selected_group,cfg

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
