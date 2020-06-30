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
from handle_Network_Devices.interface import support
Infra = Infra.Core()
DaPr = DaPr.Core()
dc = DeviceCheck()
hc = connector_async.Connection()
sf = support.SupportFunc()

class Interface:

    def __init__(self):
        self.wait_task_num = 0
        self.total_task_num = 0

    async def flow(self):
        start = time.time()
        show_title.show()
        devices,common_cfg = sf.load_config()
        # loop = asyncio.get_event_loop()
        # tasks = []
        # print(device_info)
        device_name_1 = "T1"
        device_name_2 = "T2"
        cfg_1 = {'desc': 'CiscoACXS', 'host': '10.98.102.243', 'port': 0, 'account': 1, 'device_type': 'cisco_ios', 'tasks': ['Check Cisco 3560 Status']}
        cfg_2 = {'desc': 'CiscoACXS', 'host': '10.98.102.243', 'port': 0, 'account': 1, 'device_type': 'cisco_ios', 'tasks': ['Check Cisco 3560 Status']}
        # for device_name, cfg in device_info.items():
        #     print(device_name,cfg)
        print("CSS",devices)
        tasks = [hc.task(hostname,cfg,common_cfg) for hostname,cfg in devices.items()]
        await asyncio.wait(tasks)

        # self.total_task_num, self.wait_task_num = len(device_info), len(device_info)
        # for device_name, cfg in device_info.items():
        #     task = self.execute(device_name, cfg)
        #     tasks.append(task)
        # loop.run_until_complete(asyncio.wait(tasks))
        # loop.close()



        # file_ext = '_merged_report.xlsx'
        # output_file = os.path.join(dc.report_folder_path, os.path.split(dc.report_folder_path)[-1] + file_ext)
        # mergeReports.merge_direct(dc.report_folder_path, output_file)
        # end = time.time()
        # input("[+]Done.Total process time used: {} seconds".format(int(end-start)))

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

