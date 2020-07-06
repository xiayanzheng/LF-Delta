import os
import prettytable
from common.data_hub import NdcHub
from lfcomlib.Jessica import DaPr
from lfcomlib.Jessica import Infra
from lfcomlib.Jessica import Format

DaPr = DaPr.Core()
Infra = Infra.Core()


class Cli:

    def load_config(self):
        config_file_path = DaPr.find_path_backward(os.getcwd(), 'config')
        cfg_uni_txt = "ndc_"
        cfg_ext = ".yaml"
        cfg_list = ["commands", "tasks", "groups", "accounts", "regx_rules"]
        for cfg_i in cfg_list:
            cfg_v = Infra.read_yaml(config_file_path, "{}{}{}".format(cfg_uni_txt, cfg_i, cfg_ext))
            setattr(NdcHub, cfg_i, cfg_v)
        selected_group = self.select_group(NdcHub.groups)
        return selected_group

    @staticmethod
    def select_group(groups):
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

    @staticmethod
    def set_report_folder_path():
        f_name = "NetworkDevice_{}".format(Format.CurrentTime.YYYYMMDD)
        NdcHub.report_folder_path = os.path.join(DaPr.find_path_backward(os.getcwd(), "Reports"), f_name)
        Infra.handle_folder_file_path(NdcHub.report_folder_path)
        return NdcHub.report_folder_path
