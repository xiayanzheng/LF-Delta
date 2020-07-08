import re

from handle_Network_Devices.pipline.common_process import CommonDataProcess
from lfcomlib.Jessica import Infra
from lfcomlib.Jessica import DaPr

DaPr = DaPr.Core()
Infra = Infra.Core()
cdp = CommonDataProcess()
raw_data = Infra.read_file("raw_data.txt")
while True:
    regx = input("regx:")
    methods = [method for method in dir(cdp) if "__" not in method]
    pre_proc = ''
    raw_data = getattr(cdp, "findall_single_line_data")(regx, raw_data)
    print(raw_data)
    m_data = DaPr.list_to_string(raw_data)
    data = re.findall(regx, m_data)
    print(data)
