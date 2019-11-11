import os, socket, datetime
from lfcomlib.Jessica import DaPr, Save, Numbers, InfraX
from lfcomlib.Jessica.Log import GetWindowsEventLogByWmiQuery
import winreg, psutil, platform, wmi, subprocess, netifaces

wmi_evt_qu = GetWindowsEventLogByWmiQuery()
Numbers = Numbers.Numbers()
DaPr = DaPr.DaPr()
Save = Save.Data()
from init.init_cfg import GlobalConfig

global_config = GlobalConfig()
global_config.set_value()
global_config.set_func_name()
from common.Utl import show_status

os.system("cls")
