from handle_Network_Devices.CiscoNetwork import Connection
from netmiko.ssh_exception import NetMikoTimeoutException
from lfcomlib.Jessica import DaPrCore as DaPr
from lfcomlib.Jessica import Infra as Infra
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

    def flow(self):
        device_info = self.get_device_info()
        for device_name, cfg in device_info.items():
            account = self.accounts[cfg["account"]]
            c_cfg = {
                "device_name": device_name,
                "ip": cfg['host'],
                "username": account['username'],
                "password": account['password'],
                "enablepass": account['enablepass'],
                "tasks": cfg['device_tasks']
            }
            self.get_info(**c_cfg)

    def data_clean(self, data_type, data, ):
        # lines = io.StringIO(result)
        # data = lines.read()
        # uptime = re.findall('uptime.+',data)
        # id = re.findall('\d{8}',data)
        # soft = re.findall('L3_.+\\.bin',data)
        # print('Device UPtime:', ''.join(uptime))
        # print('Device ID:', ''.join(id))
        # print('Soft Version:',''.join(soft))
        return data

    def connect_device_i(self, **cfg):
        try:
            device = self.connect_device(cfg['ip'], cfg['username'], cfg['password'], cfg['enablepass'])
            return device
        except (EOFError, NetMikoTimeoutException):
            print('Can not connect to Device')

    def get_info(self, **cfg):
        device = self.connect_device_i(**cfg)
        log_file_name = "{}_{}".format(cfg["device_name"], cfg["ip"])
        self.open_log_file(log_file_name)
        # switch.interfaceInfo('show ip int brief')
        task_list = cfg['tasks']
        for task in task_list:
            for cmd in self.tasks[task]['commands']:
                sp_line = "-----------------------------"
                title = "{}[{}]{}".format(sp_line, self.commands[cmd], sp_line)
                print(title)
                self.logfile.write("\n"+title+"\n")
                data = device.show(self.commands[cmd], True)
                if self.data_clean_enabled:
                    data = self.data_clean(cmd, data)
                self.logfile.write(data)
        device.close()
        self.close_log_file()

    def get_device_info(self):
        config_file = DaPr.Core.find_path_backward(os.getcwd(), 'config')
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

    def connect_device(self, ip, username, password, enablepass):
        device = Connection(username, password, enablepass)
        device.cisco_device(ip)
        return device

    def open_log_file(self, log_file_name):
        filepath = os.path.join(os.getcwd(), 'log\\')
        filename = "{}.txt".format(log_file_name)
        if os.path.exists(filepath):
            message = 'OK,the "{}" dir exists.'.format(filepath)
            # print(message)
        else:
            message = "Now, I will create the {}".format(filepath)
            # print(message)
            os.makedirs(filepath)
        self.logfile = open(filepath + filename, 'w')

    def close_log_file(self):
        self.logfile.close()


if __name__ == '__main__':
    dc = DeviceCheck()
    dc.flow()
