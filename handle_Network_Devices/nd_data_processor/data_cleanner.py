from lfcomlib.Jessica import DaPrCore as DaPr
from lfcomlib.Jessica import Infra
from handle_Network_Devices.nd_data_processor.common_process import CommonDataProcess
import re
import io
import os


class DataCleaner(CommonDataProcess):

    def __init__(self):
        self.base = DaPr.Core.find_path_backward(os.getcwd(), "test_data")
        self.TOT_file = self.base + "\\Cisco_TOT.txt"
        self.MEM_file = self.base + "\\Cisco_MEM.txt"
        self.TCP_file = self.base + "\\Cisco_TCP.txt"
        self.proc_func_single_line = "single_line"
        self.proc_func_multi_line = "multi_line"

    def clean(self,cmd,data):
        # TODO
        rule = None
        proc_func = None
        r_data = None
        d_func_index = {
            "cpu_usage":["3560_show_cpu"],
            "fan_status":["3560_show_fan_pwr_tem_status"],
            "tmp":["3560_show_fan_pwr_tem_status"],
            "tmp_ok":["3560_show_fan_pwr_tem_status"],
            "tmp_status":["3560_show_fan_pwr_tem_status"],
            "version":["3560_show_version"],
            "log_status":["3560_show_log"],
            "uptime":["3560_show_version"],
            "mem_status":["3560_show_mem","3560_show_proc_mem"],
            "tcp_status":["3560_show_ip_traffic"],
            "pwr_status":["3560_show_fan_pwr_tem_status"]
        }
        d_pkg = {
            "cpu_usage": {"proc_func":self.proc_func_single_line,"rule":"CPU utilization.+"},
            "fan_status": {"proc_func":self.proc_func_single_line,"rule":"FAN.+"},
            "tmp": {"proc_fun":self.proc_func_single_line,"rule":"System Temperature Value.+"},
            "tmp_ok": {"proc_fun":self.proc_func_single_line,"rule":"TEMPERATURE is.+"},
            "tmp_status": {"proc_fun":self.proc_func_single_line,"rule":"Temperature State.+"},
            "version": {"proc_fun":self.proc_func_single_line,"rule":".+Version.+RELEASE SOFTWARE"},
            "log_status": {"proc_fun":self.proc_func_single_line,"rule":"Syslog logging.+"},
            "uptime": {"proc_fun":self.proc_func_single_line,"rule":".+uptime.+"},
            "mem_status": {"proc_fun":self.proc_func_multi_line,"rule":"Processor.+.+PID"},
            "tcp_status": {"proc_fun":self.proc_func_multi_line,"rule":"TCP.+total"},
            "pwr_status": {"proc_fun":self.proc_func_multi_line,"rule":"Sys Pwr.+SW  Status"}
        }
        for k, v in d_func_index.items():
            if cmd in v:
                rule = d_pkg[k]["rule"]
                proc_func = d_pkg[k]["proc_fun"]
        if proc_func == self.proc_func_single_line:
            r_data = self.findall_single_line_data(rule,data)
        elif proc_func == self.proc_func_multi_line:
            r_data = self.convert_multiline_to_single_line(rule,data)
        return r_data
# def test():
#     dc = DataCleaner()
#     dc.clean("CHCS-CS-H01",Infra.read_file(dc.TOT_file))
#
#
# test()
