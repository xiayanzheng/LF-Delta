from handle_Network_Devices.flow.flow_master import Interface as NdCheck
from handle_server.flow import flow_master as info_collector
from interface.Delta_Launcher.delta_show_title import delta_show_title
from lfcomlib.Jessica import DaPr
from support_tools.encryption.encryption import Encrypt as MsgEncryptTool
import os
DaPr = DaPr.Core()


class Delta:

    def __init__(self):
        self.functions = [
            "run_info_collector",
            "run_nd_check",
            "run_msg_encrypt_tool"
        ]

    def starter(self):
        delta_show_title()
        table_head = ["ID", "Tool"]
        txt = "Tool ID >"
        selected = DaPr.show_selection_table(self.functions, table_head, txt)
        os.system("cls")
        getattr(self, selected)()

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
