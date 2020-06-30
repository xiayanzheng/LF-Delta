import asyncio
import netdev
from lfcomlib.Jessica import DaPr
from lfcomlib.Jessica import Infra
from lfcomlib.Jessica import Format
from handle_Network_Devices.interface import pipline
import os
DaPr = DaPr.Core()
Infra = Infra.Core()
dc = pipline.DeviceCheck()

class Connection():

    def __init__(self):
        self.commands = None
        self.tasks = 0
        self.accounts = None
        self.regx_rules = None

    async def task(self,hostname,cfg,common_cfg):
        self.commands = common_cfg['commands']
        self.tasks = common_cfg['tasks']
        self.accounts = common_cfg['accounts']
        self.regx_rules = common_cfg['regx_rules']

        await self.task_flow('',hostname,cfg)
        # async with netdev.create(**cfg) as ios:
        #     # Testing sending simple command
        print("sasa",cfg)
        title = "[+]Executing Command [{}]".format(cmd)
        cmd_cfg = self.commands[cmd]
        print(title)
        # data = await ios.send_command(cmd_cfg['cmd'])
        data = "cwd9jpa;dwdw"
        if dc.data_clean_enabled:
            data = dc.data_cleaner.clean(cmd, data, self.regx_rules, self.commands)
        data = DaPr.insert_value_to_list_and_merge(data, '-')
        return cmd_cfg, data

    async def task_flow(self,ios,hostname,cfg):
        dc.set_report_folder_path()
        regx = '[^A-Za-z0-9\u4e00-\u9fa5\\-]'
        print(cfg)
        dc.string_host_ip = "{}_{}".format(hostname, cfg["host"])
        task_list = cfg['tasks']
        dc.result_head[1] = dc.string_host_ip
        data = "test_data_dawd[wdawdwad"
        for task in task_list:
            print("sdawdw",self.tasks)
            for cmd in self.tasks[task]['commands']:
                print("CMD",cmd)
                cmd_cfg = self.commands[cmd]
                if cmd_cfg['save_to'] in ['csv', 'CSV']:
                    d_pkg = {dc.result_head[0]: cmd_cfg['cmd'], dc.result_head[1]: data}
                    dc.result_data_temp_store.append(d_pkg)
                elif cmd_cfg['save_to'] in ['txt', 'TXT']:
                    date = Format.CurrentTime.YYYYMMDD
                    log_file_path = os.path.join(dc.report_folder_path, "{}_{}".format(dc.string_host_ip, date))
                    Infra.handle_folder_file_path(log_file_path)
                    print("[+]Writing data to txt")
                    dc.export_data_to_txt(log_file_path, cmd_cfg, data)
        print("[+]Data ready")
        dc.export_data_to_csv()
        # Infra.close_file_conn(self.logfile)




