import os

from handler.handle_Network_Devices.flow.flow_master import Interface as NdCheck
from handler.handle_server.flow import flow_master as info_collector
from interface.Delta_Launcher.delta_show_title import delta_show_title
from lfcomlib.Jessica import DaPr
from support_tools.encryption.encryption import Encrypt as MsgEncryptTool

DaPr = DaPr.Core()


class Delta:

    def __init__(self):
        self.table_head = ["ID", "Tool", "Description"]
        self.txt = "Tool ID >"
        self.functions = [
            ["Server Info Collector", "..."],
            ["Network Device Checker", "..."],
            ["Message Encrypt Tool", "..."]
        ]
        self.function_map = {
            "Server Info Collector": "run_info_collector",
            "Network Device Checker": "run_nd_check",
            "Message Encrypt Tool": "run_msg_encrypt_tool"
        }

    def starter(self):
        delta_show_title()
        selected = DaPr.show_selection_table(self.functions, self.table_head, self.txt)
        os.system("cls")
        getattr(self, self.function_map[selected[1]])()

    @staticmethod
    def run_info_collector():
        info_collector.main()

    @staticmethod
    def run_nd_check():
        dc = NdCheck()
        dc.flow()

    @staticmethod
    def run_msg_encrypt_tool():
        ep = MsgEncryptTool()
        ep.main()
