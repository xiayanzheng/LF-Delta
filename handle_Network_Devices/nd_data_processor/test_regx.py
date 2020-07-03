import re
from lfcomlib.Jessica import Infra
from handle_Network_Devices.nd_data_processor.common_process import CommonDataProcess

cdp = CommonDataProcess()

Infra = Infra.Core()

def t1():
    data = "Total  System  Free  Memory.........................  (275772  KB)  269  MB  (39  %)Total  Memory  in  Buffers..........................  (864  KB)Total  Memory  in  Cache............................  (152160  KB)  148  MBTotal  Active  Memory..............................  (368572  KB)  359  MBTotal  InActive  Memory............................  (40076  KB)  39  MBTotal  Memory  in  Anon  Pages.......................  (255632  KB)  249  MBTotal  Memory  in  Slab.............................  (12740  KB)  12  MBTotal  Memory  in  Page  Tables......................  (1800  KB)  1  MBEffective  Free  Memory............................  (275884  KB)  269  MB  (39  %)WLC  Peak  Memory..................................  (811696  KB)  792  MBWLC  Virtual  Memory  Size..........................  (729628  KB)  712  MBWLC  Resident  Memory..............................  (292200  KB)  285  MBWLC  Data  Segment  Memory..........................  (633700  KB)  618  MBTotal  Heap  Including  Mapped  Pages................  (168764  KB)  164  MBTotal  Memory"
    rs = re.findall("Total.+System.+%\\)Total  Memory", data)
    print(rs)


def del_invalid_str():
    str = "(Cisco-Controller) >_"
    ss = re.sub('[^A-Za-z0-9\u4e00-\u9fa5]', '', str)
    print(ss)

def t3():
    data = Infra.read_file("E:\Documents\PD\CodeOplex\LF-Delta\config\dev\\3850堆叠的SHOW ENV ALL.txt")
    data = cdp.findall_multiline_data("SW.+", data)
    print(data)


t3()
