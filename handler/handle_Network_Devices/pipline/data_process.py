import os

from common.data_hub import NdcHub
from handler.handle_Network_Devices.pipline.data_cleanner import DataCleaner
from lfcomlib.Jessica import DaPr
from lfcomlib.Jessica import Format
from lfcomlib.Jessica import Infra
from lfcomlib.Jessica import Save

DaPr = DaPr.Core()
Infra = Infra.Core()
Save = Save.Core()


class PackDeviceData:

    def __init__(self):
        self.logfile = None
        self.data_clean_enabled = True
        self.data_cleaner = DataCleaner()
        self.report_folder_path = None
        self.report_file_name = None
        self.result_head = ['item', None]
        self.result_data_temp_store = []
        self.string_host_ip = None

    def pipeline_flow(self, cmd_name, cmd_cfg, data, **cfg):
        regx = '[^A-Za-z0-9\u4e00-\u9fa5\\-]'
        hostname = DaPr.del_invalid_str(regx, cfg["hostname"])
        real_cmd = cmd_cfg['cmd']
        host = cfg["host"]
        self.string_host_ip = "{}_{}".format(hostname, host)
        data = self.clean_data(data, cmd_name, host)
        self.export_data(data, cmd_name, real_cmd, cmd_cfg)

    def set_report_file_name(self):
        return "{}.csv".format(self.string_host_ip)

    def clean_data(self, data, cmd, host):
        title = "[+][Host:{}] Executing Command [{}]".format(host,cmd)
        print(title)
        if self.data_clean_enabled:
            data = self.data_cleaner.clean(cmd, data, NdcHub.regx_rules, NdcHub.commands)
        data = DaPr.insert_value_to_list_and_merge(data, '-')
        return data

    def export_data(self, data, cmd_name, real_cmd, cmd_cfg):
        if cmd_cfg['save_to'].lower() in ['csv']:
            self.result_head[1] = self.string_host_ip
            d_pkg = {self.result_head[0]: "{}_[{}]".format(cmd_name, real_cmd), self.result_head[1]: data}
            self.result_data_temp_store.append(d_pkg)
        elif cmd_cfg['save_to'].lower() in ['txt']:
            date = Format.CurrentTime.YYYYMMDD
            log_file_path = os.path.join(NdcHub.report_folder_path, "{}_{}".format(self.string_host_ip, date))
            Infra.handle_folder_file_path(log_file_path)
            print("[+]Writing data to txt")
            self.export_data_to_txt(log_file_path, cmd_cfg, data)

    @staticmethod
    def export_data_to_txt(log_file_path, cmd_cfg, data):
        try:
            filename = "{}.txt".format(cmd_cfg['cmd'])
            logfile = Infra.open_file_conn(log_file_path, filename)
            logfile.write(data)
            logfile.close()
            return True
        except Exception as e:
            print("[!]Unable crate file.Err-Msg:{}".format(e))
            return False
            pass

    def export_data_to_csv(self):
        print("[+]Writing data to csv")
        Save.to_csv(self.result_head, self.result_data_temp_store, NdcHub.report_folder_path,
                    self.set_report_file_name())
        self.result_data_temp_store = []

    @staticmethod
    def show_progress():
        total = NdcHub.total_task_num
        wait = NdcHub.wait_task_num
        print("[+]Task status:Total {},Wait {}".format(total, wait))
