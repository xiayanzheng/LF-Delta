from handle_Network_Devices.cisco.connector import Connection
from netmiko.ssh_exception import NetMikoTimeoutException
from lfcomlib.Jessica import DaPrCore as DaPr
from lfcomlib.Jessica import Infra as Infra
from lfcomlib.Jessica import Format
from handle_Network_Devices.nd_data_processor.data_cleanner import DataCleaner
import prettytable
import os


class DeviceCheck(Connection):

    def __init__(self):
        self.commands = None
        self.tasks = None
        self.groups = None
        self.accounts = None
        self.logfile = None
        self.data_clean_enabled = True
        self.data_cleaner = DataCleaner()
        self.DaPr = DaPr.Core()
        self.log_file_path = os.path.join(os.getcwd(), 'log\\')

    def flow(self):
        device_info = self.get_device_info()
        for device_name, cfg in device_info.items():
            account = self.accounts[cfg["account"]]
            cfg["ip"] = cfg['host']
            cfg["device_name"] = device_name
            cfg["username"] = account['username']
            cfg["password"] = account['password']
            cfg["enablepass"] = account['enablepass']
            self.get_info(**cfg)

    def data_clean(self, cmd, data):
        # lines = io.StringIO(result)
        # data = lines.read()
        # uptime = re.findall('uptime.+',data)
        # id = re.findall('\d{8}',data)
        # soft = re.findall('L3_.+\\.bin',data)
        # print('Device UPtime:', ''.join(uptime))
        # print('Device ID:', ''.join(id))
        # print('Soft Version:',''.join(soft))
        data = self.data_cleaner.clean(cmd, data)
        data = self.DaPr.insert_value_to_list_and_merge(data,"-")
        print(data)
        return data

    def connect_device_i(self, **cfg):
        try:
            device = self.connect_device(**cfg)
            cfg["hostname"] = device.get_hostname()
            return cfg,device
        except (EOFError, NetMikoTimeoutException):
            print('Can not connect to Device')

    def set_file_name(self,**cfg):
        log_file_name = "{}_{}_{}".format(cfg["hostname"], cfg["ip"],Format.CurrentTime.YYYYMMDD)
        filename = "{}.txt".format(log_file_name)
        return filename

    def get_info(self, **cfg):
        cfg,device = self.connect_device_i(**cfg)
        self.logfile = Infra.open_file_conn(self.log_file_path, self.set_file_name(**cfg))
        # switch.interfaceInfo('show ip int brief')
        task_list = cfg['tasks']
        for task in task_list:
            for cmd in self.tasks[task]['commands']:
                sp_line = "-----------------------------"
                title = "{}[{}]{}".format(sp_line, self.commands[cmd], sp_line)
                print(title)
                self.logfile.write("\n" + title + "\n")
                data = device.show(self.commands[cmd], True)
                if self.data_clean_enabled:
                    data = self.data_clean(cmd,data)
                self.logfile.write(data)
        device.close()
        Infra.close_file_conn(self.logfile)

    def get_device_info(self):
        config_file = self.DaPr.find_path_backward(os.getcwd(), 'config')
        cfg = Infra.read_json(config_file, 'network_device_config.json')
        self.commands = cfg["commands"]
        self.tasks = cfg["tasks"]
        self.groups = cfg["groups"]
        self.accounts = cfg["accounts"]
        selected_group = self.select_group(self.groups)
        return selected_group
        # print(tasks)
        # print(cfg["groups"])

    def select_group(self, groups):
        group_list = []
        for k, v in groups.items():
            group_list.append(k)
        pt = prettytable.PrettyTable()
        pt.field_names = ["No", "Group"]
        for i in range(len(group_list)):
            no = i
            group = group_list[i]
            pt.add_row([no, group])
        print(pt)
        selected = int(input("pls select a group："))
        return groups[group_list[selected]]



if __name__ == '__main__':
    dc = DeviceCheck()
    dc.flow()
