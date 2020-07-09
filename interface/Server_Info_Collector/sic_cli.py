import os
import prettytable
from init.init_imports import global_config as gc
from lfcomlib.Jessica import Infra
from lfcomlib.Jessica import DaPr
from interface.Server_Info_Collector.show_sic_title import show_sic_title
Infra = Infra.Core()
DaPr = DaPr.Core()


class SicCli:

    @staticmethod
    def intro():
        show_sic_title()

    def add_group(self):
        new_group_name = str(input("Pls input a new group name："))
        new_group_list = gc.app_config['group']
        if new_group_name in new_group_list:
            print("Group Name exists")
            self.select_group()
        new_group_list.append(new_group_name)
        gc.app_config['group'] = new_group_list
        Infra.write_json(gc.config_root, gc.app_config_file_name, gc.app_config)
        gc.group = gc.app_config['group']
        self.select_group()

    def select_group(self):
        self.intro()
        group_list = gc.group
        new_group_dict = {}
        pt = prettytable.PrettyTable()
        pt.field_names = ['No.', 'GroupName']
        for i in range(len(group_list)):
            no = str(i)
            name = group_list[i]
            pt.add_row([no, name])
            new_group_dict[no] = group_list[i]
        print(pt)
        info = "Please select a number from [No]\nif group name is not in this table pls input [a] to add a group："
        user_selected = input(info)
        if user_selected in ['a', 'A']:
            self.add_group()
        if user_selected in list(new_group_dict.keys()):
            selected_group = new_group_dict[str(user_selected)]
            return selected_group
        else:
            print("Group not exits")
            self.select_group()

    def init_merge_report_path(self, group_name):
        report_root = DaPr.find_path_backward(os.getcwd(), 'Reports')
        report_objs = os.listdir(report_root)
        pt = prettytable.PrettyTable()
        pt.field_names = ['No', 'Report Name']
        repo_selections = {}
        count = 1
        for i in range(len(report_objs)):
            if group_name in report_objs[i]:
                index = str(count)
                repo_name = report_objs[i]
                print(">>", repo_name)
                if os.path.isdir(os.path.join(report_root, repo_name)):
                    pt.add_row([index, repo_name])
                    repo_selections[index] = repo_name
                    count += 1
        print(pt)
        selected = input("Pls select a record：")
        if selected in list(repo_selections.keys()):
            report_objs_dev = os.path.join(report_root, repo_selections[selected])
            report_objs_dev_objs = os.listdir(report_objs_dev)
            return report_root, report_objs, report_objs_dev, report_objs_dev_objs
        else:
            print("Selected Group is not exists")
            self.init_merge_report_path(group_name)



