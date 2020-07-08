import os

import prettytable

from lfcomlib.Jessica import Infra

Infra = Infra.Core()


class BuildTools:

    def __init__(self):
        self.builder = "D:\\Python374\\Scripts\\pyinstaller.exe"
        self.root = "E:\\Documents\\PD\\CodeOplex\\LF-Delta"
        self.tools = [
            "build_info_collector",
            "build_network_device_check",
            "build_msg_encrypt_tool"
        ]

    def build(self):
        pt = prettytable.PrettyTable()
        pt.field_names = ["ID", "Tool"]
        for i in range(len(self.tools)):
            no = i
            tool = self.tools[i]
            pt.add_row([no, tool])
        print(pt)
        selected = input("Tool ID >")
        getattr(self, self.tools[int(selected)])()

    def build_info_collector(self):
        tool_name = "infoCollector"
        params = "-F "
        target = "{}\\{}.py".format(self.root, tool_name)
        dis_dir = "{}\\dist\\".format(self.root)
        user_dist = "{}{}\\".format(dis_dir, tool_name)
        app_cfg_dir = "{}\\config".format(self.root)
        support_files = [os.path.join(self.root, 'config')]

        app_cfg = Infra.read_json(app_cfg_dir, 'app_config.json')
        version = app_cfg['version']
        print(version)
        Infra.remove_ff(dis_dir)
        os.system("{} {} {}".format(self.builder, target, params))
        sga_name = os.path.join(dis_dir, tool_name)
        if "onefile" in params:
            sga_name = "{}{}".format(sga_name, '.exe')
            Infra.copy_ff(sga_name, user_dist)
        for s_file in support_files:
            Infra.copy_ff(s_file, user_dist)
        Infra.open_dir(dis_dir)

    def build_network_device_check(self):
        params = "-F --hidden-import win32timezone "
        os.system("{} {} {}".format(self.builder, params, "NDCheck.py"))

    def build_msg_encrypt_tool(self):
        params = "-F --hidden-import win32timezone "
        os.system("{} {} {}".format(self.builder, params, "MsgEncryptTool.py"))


bt = BuildTools()
bt.build()
