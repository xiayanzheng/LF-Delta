import os

import prettytable

from common.data_hub import NdcHub
from common.data_hub import Salt
from lfcomlib.Jessica import DaPr
from lfcomlib.Jessica import Format
from lfcomlib.Jessica import Infra
from lfcomlib.Jessica import Security
from lfcomlib.Jessica.Log import simple_err_log

DaPr = DaPr.Core()
Infra = Infra.Core()
Security = Security.Core()


class Cli:

    def load_config(self):
        config_file_path = DaPr.find_path_backward(os.getcwd(), 'config')
        app_config = Infra.read_yaml(config_file_path, "ndc_app_config.yaml")
        config_index = app_config['config_file_location']
        config_report_root = app_config['report_file_root']
        cfg_list = ["commands", "tasks", "groups", "accounts", "regx_rules"]
        for cfg_i in cfg_list:
            file = config_index[cfg_i]
            if "\\" in file or "/" in file and os.path.isdir(file):
                cfg_v = Infra.read_yaml(config_index[cfg_i])
            else:
                cfg_v = Infra.read_yaml(config_file_path, "{}".format(config_index[cfg_i]))
            setattr(NdcHub, cfg_i, cfg_v)
        self.repack_account()
        selected_group_name, selected_group = self.select_group(NdcHub.groups)
        return selected_group_name, selected_group, config_report_root

    @staticmethod
    def select_group(groups):
        group_list = []
        for k, v in groups.items():
            group_list.append({"group": k, "nod": len(v.items())})
        pt = prettytable.PrettyTable()
        pt.field_names = ["ID", "Group", "Number of Devices"]
        for i in range(len(group_list)):
            no = i
            group = group_list[i]['group']
            nod = group_list[i]['nod']
            pt.add_row([no, group, nod])
        print(pt)
        selected = int(input("[>]Pls select a group by ID："))
        selected_group_name = group_list[selected]["group"]
        return selected_group_name, groups[selected_group_name]

    @staticmethod
    def set_report_folder_path(selected_group_name, config_report_root):
        f_name = "{}_{}".format(selected_group_name, Format.CurrentTime.YYYYMMDD)
        config_report_root_r = DaPr.find_path_backward(os.getcwd(), "Reports")
        if "\\" in config_report_root or "/" in config_report_root and os.path.isdir(config_report_root):
            config_report_root_r = config_report_root
        NdcHub.report_folder_path = os.path.join(config_report_root_r, f_name)
        Infra.handle_folder_file_path(NdcHub.report_folder_path)
        return NdcHub.report_folder_path

    @staticmethod
    @simple_err_log()
    def repack_account():
        accounts = NdcHub.accounts
        try:
            decrypt_accounts = {}
            for k, v in accounts.items():
                new_inner = {}
                for k2, v2 in v.items():
                    key = Security.decrypt(Salt.sec, v2)
                    new_inner[k2] = key.decode()
                decrypt_accounts[k] = new_inner
            NdcHub.accounts = decrypt_accounts
        except:
            pass
