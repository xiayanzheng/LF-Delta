import os
import prettytable
from common.data_hub import NdcHub
from lfcomlib.Jessica import DaPr
from lfcomlib.Jessica import Infra

DaPr = DaPr.Core()
Infra = Infra.Core()


class Cli:

    def load_config(self):
        config_file_path = DaPr.find_path_backward(os.getcwd(), 'config')
        cfg = Infra.read_yaml(config_file_path, 'network_device_config.yaml')
        NdcHub.commands = cfg["commands"]
        NdcHub.tasks = cfg["tasks"]
        NdcHub.groups = cfg["groups"]
        NdcHub.accounts = cfg["accounts"]
        NdcHub.regx_rules = cfg["regx_rules"]
        selected_group = self.select_group(NdcHub.groups)
        return selected_group

    def select_group(self, groups):
        group_list = []
        for k, v in groups.items():
            group_list.append(k)
        pt = prettytable.PrettyTable()
        pt.field_names = ["ID", "Group"]
        for i in range(len(group_list)):
            no = i
            group = group_list[i]
            pt.add_row([no, group])
        print(pt)
        selected = int(input("[>]Pls select a group by ID："))
        return groups[group_list[selected]]


