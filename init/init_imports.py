import os, socket, datetime, asyncio, prettytable
from lfcomlib.Jessica import DaPr, Save, Numbers, Infra
from lfcomlib.Jessica.Log import GetWindowsEventLogByWmiQuery
import winreg, psutil, platform, wmi, subprocess, netifaces
from init.init_cfg import GlobalConfig

wmi_evt_qu = GetWindowsEventLogByWmiQuery()
Numbers = Numbers.Numbers()
global_config = GlobalConfig()
global_config.set_value()
from common.Utl import show_status

os.system("cls")
