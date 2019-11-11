from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.cisco_base_connection import CiscoBaseConnection
import time
import sys
import getpass
import re
import io
import os


# import StringIO

class CiscoNetwork(CiscoBaseConnection):
    def __init__(self, username, password, enablepass):
        self.username = username
        self.password = password
        self.enablepass = enablepass

    def CiscoDevice(self, iplist):
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

    def gethostname(self):
        self.hostname = self.connect.find_prompt()
        self.hostname = self.hostname.replace("#", "")
        print(self.hostname)

    '''     
    def interfaceInfo(self,cmd):
        result = self.connect.send_command(cmd)
        for interface in result.split('\n'):
            if 'up' in interface:
                #print interface
                lines=io.StringIO(interface)
                data = lines.read()
                intername = ' '.join(re.findall('^Eth.+\/\d',data))
                loopback  = ' '.join(re.findall('Loopback[0-9]',data))
                interIP = re.findall( '\.'.join(['\d{1,3}']*4),data)
                if intername:
                    print(intername ,':', ''.join(interIP))
                else:
                    print(loopback  , ':', ''.join(interIP))
    '''

    def show(self, cmd):
        result = self.connect.send_command(cmd)
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

        filepath = 'D:\\96. Other\\04. Development\\960401. python\\Python37\\AutomaticInspection\\log\\'
        filename = 'log.txt'

        if os.path.exists(filepath):
            message = 'OK,the  "%s" dir exists.'
        else:
            message = "Now, I will create the %s"
            os.makedirs(filepath)
        save = open(filepath + filename, 'w')
        save.write(result)
        save.close()

    def close(self):
        if self.connect is not None:
            self.connect.disconnect()
            self.connect = None


if __name__ == '__main__':
    print("[+] This Program is beging done.......")
    username = input('Username:')
    password = getpass.getpass()
    enablepass = input('enablepass:')
    # for iplist in open("/opt/other/ip.txt"):'''
    try:
        switch = CiscoNetwork(username, password, enablepass)
        switch.CiscoDevice('10.98.102.254')
        switch.gethostname()
        # switch.interfaceInfo('show ip int brief')
        switch.show('show config')
        switch.close()
    except (EOFError, NetMikoTimeoutException):
        print('Can not connect to Device')
