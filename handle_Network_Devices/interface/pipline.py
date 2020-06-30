from handle_Network_Devices.cisco.connector import Connection
from netmiko.ssh_exception import NetMikoTimeoutException
from lfcomlib.Jessica import DaPr
from lfcomlib.Jessica import Infra
from lfcomlib.Jessica import Format
from lfcomlib.Jessica import Save
from handle_Network_Devices.nd_data_processor.data_cleanner import DataCleaner
import os

DaPr = DaPr.Core()
Infra = Infra.Core()
Save = Save.Core()


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
        self.result_head = ['item', None]
        self.result_data_temp_store = []
        self.string_host_ip = None

    def set_report_folder_path(self):
        f_name = "NetworkDevice_{}".format(Format.CurrentTime.YYYYMMDD)
        self.report_folder_path = os.path.join(DaPr.find_path_backward(os.getcwd(), "Reports"), f_name)
        if not os.path.exists(self.report_folder_path):
            Infra.create_folder(self.report_folder_path)
        return self.report_folder_path

    def set_report_file_name(self):
        return "{}.csv".format(self.string_host_ip)

    def connect_device_i(self, **cfg):
        try:
            device = self.connect_device(**cfg)
            cfg["hostname"] = device.get_hostname()
            print("[+]Device Connected")
            return cfg, device
        except (EOFError, NetMikoTimeoutException):
            print('[!]Can not connect to Device')

    def command_executor(self, device, cmd):
        title = "[+]Executing Command [{}]".format(cmd)
        cmd_cfg = self.commands[cmd]
        print(title)
        data = device.show(cmd_cfg['cmd'], True)
        if self.data_clean_enabled:
            data = self.data_cleaner.clean(cmd, data, self.regx_rules, self.commands)
        data = DaPr.insert_value_to_list_and_merge(data, '-')
        return cmd_cfg, data

    def export_data_to_txt(self, log_file_path, cmd_cfg, data):
        try:
            filename = "{}.txt".format(cmd_cfg['cmd'])
            logfile = Infra.open_file_conn(log_file_path, filename)
            logfile.write(data)
            logfile.close()
            return True
        except:
            print("[!]Unable crate file")
            return False
            pass

    def export_data_to_csv(self):
        print("[+]Writing data to csv")
        Save.toCSV(self.result_head, self.result_data_temp_store, self.report_folder_path,
                   self.set_report_file_name())
        self.result_data_temp_store = []
        return True

    def get_info(self, **cfg):
        cfg, device = self.connect_device_i(**cfg)
        self.set_report_folder_path()
        regx = '[^A-Za-z0-9\u4e00-\u9fa5\\-]'
        hostname = DaPr.del_invalid_str(regx, cfg["hostname"])
        self.string_host_ip = "{}_{}".format(hostname, cfg["ip"])
        task_list = cfg['tasks']
        self.result_head[1] = self.string_host_ip
        for task in task_list:
            for cmd in self.tasks[task]['commands']:
                cmd_cfg, data = self.command_executor(device, cmd)
                if cmd_cfg['save_to'] in ['csv', 'CSV']:
                    d_pkg = {self.result_head[0]: cmd_cfg['cmd'], self.result_head[1]: data}
                    self.result_data_temp_store.append(d_pkg)
                elif cmd_cfg['save_to'] in ['txt', 'TXT']:
                    date = Format.CurrentTime.YYYYMMDD
                    log_file_path = os.path.join(self.report_folder_path, "{}_{}".format(self.string_host_ip, date))
                    Infra.handle_folder_file_path(log_file_path)
                    print("[+]Writing data to txt")
                    self.export_data_to_txt(log_file_path, cmd_cfg, data)
        device.close()
        print("[+]Device Disconnected")
        # print(self.set_report_folder_path(), self.set_file_name())
        print("[+]Data ready")
        self.export_data_to_csv()
        # Infra.close_file_conn(self.logfile)
