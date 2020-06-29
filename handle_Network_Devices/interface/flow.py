from handle_Network_Devices.cisco.connector import Connection
from netmiko.ssh_exception import NetMikoTimeoutException
from init.init_imports import DaPrX
from init.init_imports import InfraX
from init.init_imports import Format
from handle_Network_Devices.nd_data_processor.data_cleanner import DataCleaner
import prettytable
import os
from init.init_imports import SaveX
from handle_report import mergeReports


class DeviceCheck(Connection):

    def __init__(self):
        self.commands = None
        self.tasks = None
        self.groups = None
        self.accounts = None
        self.regx_rules = None
        self.logfile = None
        self.data_clean_enabled = True
        self.data_cleaner = DataCleaner()
        self.report_folder_path = None
        self.report_file_name = None
        self.log_file_path = os.path.join(os.getcwd(), 'log\\')
        self.result_head = ['item', None]
        self.result_data_temp_store = []
        self.string_host_ip = None

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
        mergeReports.merge_dirct(self.report_folder_path)

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
        return data

    def connect_device_i(self, **cfg):
        try:
            device = self.connect_device(**cfg)
            cfg["hostname"] = device.get_hostname()
            return cfg, device
        except (EOFError, NetMikoTimeoutException):
            print('Can not connect to Device')

    def set_file_name(self):
        filename = "{}_{}.txt".format(self.string_host_ip, Format.CurrentTime.YYYYMMDD)
        return filename

    def set_report_folder_path(self):
        f_name = "NetworkDevice_{}".format(Format.CurrentTime.YYYYMMDD)
        self.report_folder_path = os.path.join(DaPrX.find_path_backward(os.getcwd(), "Reports"), f_name)
        if not os.path.exists(self.report_folder_path):
            InfraX.create_folder(self.report_folder_path)
        return self.report_folder_path

    def set_report_file_name(self, **cfg):
        return "{}.csv".format(self.string_host_ip)

    def get_info(self, **cfg):
        cfg, device = self.connect_device_i(**cfg)
        self.string_host_ip = "{}_{}".format(cfg["desc"], cfg["ip"])
        # self.logfile = InfraX.open_file_conn(self.log_file_path, self.set_file_name())
        # switch.interfaceInfo('show ip int brief')
        task_list = cfg['tasks']
        self.result_head[1] = self.string_host_ip
        for task in task_list:
            for cmd in self.tasks[task]['commands']:
                sp_line = "-----------------------------"
                title = "{}[{}]{}".format(sp_line, cmd, sp_line)
                print(title)
                # self.logfile.write("\n" + title + "\n")
                data = device.show(self.commands[cmd]['cmd'], True)
                if self.data_clean_enabled:
                    data = self.data_cleaner.clean(cmd,data,self.regx_rules,self.commands)
                # self.logfile.write(data)
                data = DaPrX.insert_value_to_list_and_merge(data, '-')
                self.result_data_temp_store.append({self.result_head[0]: self.commands[cmd]['cmd'],
                                                    self.result_head[1]: data})
        device.close()
        # print(self.set_report_folder_path(), self.set_file_name())
        SaveX.toCSV(self.result_head, self.result_data_temp_store, self.set_report_folder_path(),
                   self.set_report_file_name())
        self.result_data_temp_store = []
        # Infra.close_file_conn(self.logfile)

    def get_device_info(self):
        config_file_path = DaPrX.find_path_backward(os.getcwd(), 'config')
        cfg = InfraX.read_yaml(config_file_path, 'network_device_config.yaml')
        self.commands = cfg["commands"]
        self.tasks = cfg["tasks"]
        self.groups = cfg["groups"]
        self.accounts = cfg["accounts"]
        self.regx_rules = cfg["regx_rules"]
        selected_group = self.select_group(self.groups)
        return selected_group

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
