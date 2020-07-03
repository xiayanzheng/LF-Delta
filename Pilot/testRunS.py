#!/usr/bin/env python
import datetime
import re
import subprocess

today = datetime.date.today().strftime('%Y%m%d')

ip = "10.98.102.254"
passwd = "Hiamscs123"

cmd = "ping {}".format(ip)
p = subprocess.Popen(cmd,
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     shell=True)
for line in iter(p.stdout.readline, b''):
    de_line = line.decode('gb2312')
    print(de_line)
    fd = re.findall(r'\b\d+\b', de_line)
    rc = re.findall(r'=(.*?ms)', de_line)
    print(fd, rc)
p.stdout.close()
p.wait()
