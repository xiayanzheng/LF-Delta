import re

from lfcomlib.Jessica import Infra
from handle_Network_Devices.nd_data_processor.common_process import CommonDataProcess

Infra = Infra.Core()
cdp = CommonDataProcess()
raw_data = Infra.read_file("raw_data.txt")
while True:
    regx = input("regx:")
    raw_data = getattr(cdp,"findall_single_line_data")(regx,raw_data)
    print(raw_data)
    data = re.findall(regx, raw_data)
    print(data)