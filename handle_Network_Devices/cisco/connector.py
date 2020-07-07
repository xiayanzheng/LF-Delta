import io
import re

from netmiko import ConnectHandler
from netmiko.cisco_base_connection import CiscoBaseConnection


# import StringIO


class Connection(CiscoBaseConnection):

    def __init__(self, username, password, enablepass, device_type):
        self.username = username
        self.password = password
        self.enablepass = enablepass
        self.device_type = device_type
        self.hostname = None

    @staticmethod
    def connect_device(**cfg):
        ip = cfg['host']
        username = cfg['username']
        password = cfg['password']
        enable_pass = cfg['enablepass']
        device_type = cfg['device_type']
        device = Connection(username, password, enable_pass, device_type)
        device.cisco_device(ip)
        return device

    def cisco_device(self, iplist):
        self.device = {
            'device_type': self.device_type,
            'username': self.username,
            'password': self.password,
            'ip': iplist,
            'secret': self.enablepass
        }
        print("[+]connect to network device... %s" % iplist)
        self.connect = ConnectHandler(**self.device)
        self.connect.enable()

    def get_hostname(self):
        self.hostname = self.connect.find_prompt()
        self.hostname = self.hostname.replace("#", "")
        return self.hostname

    def interface_info(self, cmd):
        result = self.connect.send_command(cmd)
        for interface in result.split('\n'):
            if 'up' in interface:
                # print flow
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
        return result

    def close(self):
        if self.connect is not None:
            self.connect.disconnect()
            self.connect = None
