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
        reports_folder = Infra.handle_folder_file_path(DaPr.find_path_backward(os.getcwd(), "Reports"))
        print(reports_folder)
        self.report_folder_path = os.path.join(reports_folder, f_name)
        if not os.path.exists(self.report_folder_path):
            Infra.create_folder(self.report_folder_path)
        return self.report_folder_path

    def set_report_file_name(self):
        return "{}.csv".format(self.string_host_ip)

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
