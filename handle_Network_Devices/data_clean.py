from lfcomlib.Jessica import DaPrCore as DaPr
from lfcomlib.Jessica import Infra as Infra
import re, io

file = open("E:\Documents\PD\CodeOplex\LF-Delta\handle_Network_Devices\Cisco_10.98.102.249.txt", 'r')
data = file.read()
# print(data.split("\n"))
lines = io.StringIO(data)
data = lines.read()
uptime = re.findall('CPU utilization.+', data)
fan = re.findall("FAN is.+", data)
tmp = re.findall("System Temperature Value.+", data)
tmp_ok = re.findall("TEMPERATURE is.+", data)
tmp_sta = re.findall("Temperature State.+", data)
ver = re.findall(".+Version.+RELEASE SOFTWARE", data)
# TODO
pwr = re.findall("Built-in", data)
pkg_rev = re.findall("TCP statistics:", data)
print(pkg_rev)
