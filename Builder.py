import os
from init.init_imports import Infra

builder = "D:\\Python374\\Scripts\\pyinstaller.exe"
root = "E:\\Documents\\PD\\CodeOplex\\LF-Delta"
params = "--onefile"
target = "{}\\infoCollector.py".format(root)
dis_dir = "{}\\dist\\".format(root)
app_cfg_dir = "{}\\config".format(root)

app_cfg = Infra.read_json(app_cfg_dir,'app_config.json')
version = app_cfg['version']
print(version)
Infra.remove_ff(dis_dir)
os.system("{} {} {}".format(builder, target, params))
os.system("explorer.exe {}".format(dis_dir))
