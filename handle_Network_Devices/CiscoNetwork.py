from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.cisco_base_connection import CiscoBaseConnection
import time
import sys
import getpass
import re
import io
import os
from lfcomlib.Jessica import DaPrCore as DaPr
from lfcomlib.Jessica import Infra as Infra
import prettytable


# import StringIO

class CiscoNetwork(CiscoBaseConnection):
    def __init__(self, username, password, enablepass):
        self.username = username
        self.password = password
        self.enablepass = enablepass

    def cisco_device(self, iplist):
        self.device = {
            'device_type': 'cisco_ios',
            'username': self.username,
            'password': self.password,
            'ip': iplist,
            'secret': self.enablepass
        }
        print('-' * 100)
        print("[+]connect to network device... %s" % iplist)
        self.connect = ConnectHandler(**self.device)
        self.connect.enable()

    def get_hostname(self):
        self.hostname = self.connect.find_prompt()
        self.hostname = self.hostname.replace("#", "")
        print(self.hostname)

    def interface_info(self, cmd):
        result = self.connect.send_command(cmd)
        for interface in result.split('\n'):
            if 'up' in interface:
                # print interface
                lines = io.StringIO(interface)
                data = lines.read()
                intername = ' '.join(re.findall('^Eth.+\/\d', data))
                loopback = ' '.join(re.findall('Loopback[0-9]', data))
                interIP = re.findall('\.'.join(['\d{1,3}'] * 4), data)
                if intername:
                    print(intername, ':', ''.join(interIP))
                else:
                    print(loopback, ':', ''.join(interIP))

    def show(self, cmd, data_clean):
        result = self.connect.send_command(cmd)
        if data_clean:
            result = self.data_clean(cmd, result)
        return result

    def data_clean(self, data_type, data, ):
        '''
             lines = io.StringIO(result)
             data = lines.read()
             uptime = re.findall('uptime.+',data)
             id = re.findall('\d{8}',data)
             soft = re.findall('L3_.+\\.bin',data)
             print('Device UPtime:', ''.join(uptime))
             print('Device ID:', ''.join(id))
             print('Soft Version:',''.join(soft))
        '''
        return data

    def close(self):
        if self.connect is not None:
            self.connect.disconnect()
            self.connect = None


class DeviceCheck(CiscoNetwork):

    def __init__(self):
        self.commands = None
        self.tasks = None
        self.groups = None
        self.accounts = None
        self.logfile = None

    def flow(self):
        device_info = self.get_device_info()
        for device_name, cfg in device_info.items():
            account = self.accounts[cfg["account"]]
            c_cfg = {
                "device_name": device_name,
                "ip": cfg['host'],
                "username": account['username'],
                "password": account['password'],
                "enablepass": account['enablepass'],
                "tasks": cfg['device_tasks']
            }
            self.get_info(**c_cfg)

    def connect_device_i(self, **cfg):
        try:
            device = self.connect_device(cfg['ip'], cfg['username'], cfg['password'], cfg['enablepass'])
            print(device.get_hostname())
            return device
        except (EOFError, NetMikoTimeoutException):
            print('Can not connect to Device')

    def get_info(self, **cfg):
        log_file_name = "{}_{}".format(cfg["device_name"], cfg["ip"])
        self.open_log_file(log_file_name)
        device = self.connect_device_i(**cfg)
        # switch.interfaceInfo('show ip int brief')
        task_list = cfg['tasks']
        for task in task_list:
            for cmd in self.tasks[task]['commands']:
                sp_line = "-----------------------------"
                title = "{}[{}]{}".format(sp_line, self.commands[cmd], sp_line)
                print(title)
                self.logfile.write(title+"\n")
                print(self.commands[cmd])
                data = device.show(self.commands[cmd], True)
                self.logfile.write(data)
        device.close()
        self.close_log_file()

    def get_device_info(self):
        config_file = DaPr.Core.find_path_backward(os.getcwd(), 'config')
        cfg = Infra.read_json(config_file, 'network_device_config.json')
        self.commands = cfg["commands"]
        self.tasks = cfg["tasks"]
        self.groups = cfg["groups"]
        self.accounts = cfg["accounts"]
        selected_group = self.select_group(self.groups)
        return selected_group
        # print(tasks)
        # print(cfg["groups"])

    def select_group(self, groups):
        group_list = []
        for k, v in groups.items():
            group_list.append(k)
        pt = prettytable.PrettyTable()
        pt.field_names = ["No", "Group"]
        for i in range(len(group_list)):
            no = i
            group = group_list[i]
            pt.add_row([no, group])
        print(pt)
        selected = int(input("pls select a group："))
        return groups[group_list[selected]]

    def connect_device(self, ip, username, password, enablepass):
        device = CiscoNetwork(username, password, enablepass)
        device.cisco_device(ip)
        return device

    def open_log_file(self, log_file_name):
        filepath = os.path.join(os.getcwd(), 'log\\')
        filename = "{}.txt".format(log_file_name)
        if os.path.exists(filepath):
            message = 'OK,the "{}" dir exists.'.format(filepath)
            # print(message)
        else:
            message = "Now, I will create the {}".format(filepath)
            # print(message)
            os.makedirs(filepath)
        self.logfile = open(filepath + filename, 'w')

    def close_log_file(self):
        self.logfile.close()


if __name__ == '__main__':
    dc = DeviceCheck()
    dc.flow()
