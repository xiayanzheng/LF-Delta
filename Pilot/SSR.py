#!/usr/bin/env python
import pexpect
from pexpect import popen_spawn
import os
import datetime
import time

today = datetime.date.today().strftime('%Y%m%d')

ip = "10.98.102.254"
passwd = "Hiamscs123"
fout = open('mylog.txt', 'wb+')
child = pexpect.popen_spawn.PopenSpawn('telnet {}'.format(ip))
child.logfile = fout
try:
    time.sleep(1)
    child.expect("Username:")
    child.sendline("root")
    time.sleep(1)
    child.expect('(?i)ssword:')
    child.sendline("Hiamscs123")
    time.sleep(1)
    print(child.before)
    print(child.after)
    # i = child.expect(['Username:', 'User Access Verification'], timeout=5)
    #
    # child.sendline("test")
except pexpect.EOF or pexpect.TIMEOUT:
    print("EOF")