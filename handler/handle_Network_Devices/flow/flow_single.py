from func_timeout import func_set_timeout
from netmiko.ssh_exception import NetMikoTimeoutException

from common.data_hub import NdcHub
from handler.handle_Network_Devices.cisco.connector import Connection
from handler.handle_Network_Devices.pipline.data_process import PackDeviceData


class Dec:

    @staticmethod
    def task(cfg):
        pdd = PackDeviceData()
        for device_cfg in cfg:
            conn = Connect("", "", "", "")
            device = conn.connect_device_i(**device_cfg)
            device_cfg["hostname"] = device.get_hostname()
            task_list = device_cfg['tasks']
            for task_i in task_list:
                for cmd_name in NdcHub.tasks[task_i]['commands']:
                    cmd_cfg = NdcHub.commands[cmd_name]
                    real_cmd = cmd_cfg['cmd']
                    data = device.show(real_cmd, True)
                    pdd.pipeline_flow(cmd_name, cmd_cfg, data, **device_cfg)
        pdd.export_data_to_csv()


class Connect(Connection):

    @func_set_timeout(20)
    def connect_device_i(self, **cfg):
        try:
            device = self.connect_device(**cfg)
            print("[+]Device Connected")
            return device
        except (EOFError, NetMikoTimeoutException):
            print('[!]Can not connect to Device')
