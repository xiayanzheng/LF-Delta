from handle_server.pipeline import get_server_info
from init.init_imports import global_config as gc
from handle_report import mergeReports
import socket
import os
import datetime


class CommonProcess(get_server_info.Entry):

    def get_server_data(self, log_path):
        self.get_basic_info(log_path, 'host_basic_data.csv')
        self.get_kav_update_status()
        self.get_disk_partitions(log_path, 'disk_info.csv')
        self.get_license_key(log_path, 'license.csv')
        self.get_installed_software(log_path, 'installed_software.csv')
        default_gateway = self.all_data['default_gateway']
        self.get_ping_result(default_gateway, log_path, 'ping_{}.txt'.format(default_gateway))
        self.get_windows_update_status(log_path, 'installed_win_updates.csv')
        event_log_cfg = gc.windows_event_config
        self.get_event_log(event_log_cfg, log_path, 'windows_event_log.csv')
        self.get_summary(log_path, 'summary.csv')

    @staticmethod
    def set_path_and_select_group(group_name):
        hostname = socket.getfqdn(socket.gethostname())
        if not os.path.exists(".\\Reports\\"):
            os.mkdir(".\\Reports\\")
        log_folder = "{}_{}".format(group_name, datetime.datetime.now().strftime('%Y-%m-%d'))
        gc.curr_log_folder = log_folder
        log_path = '.\\Reports\\{}\\{}'.format(log_folder, hostname)
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        return log_path, log_folder

    @staticmethod
    def merge_reports(group_name):
        return mergeReports.merge(group_name)

