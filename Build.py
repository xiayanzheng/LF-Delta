import os

from init.init_imports import Infra

builder = "D:\\Python374\\Scripts\\pyinstaller.exe"
root = "E:\\Documents\\PD\\CodeOplex\\LF-Delta"
tool_name = "infoCollector"
params = ""
target = "{}\\{}.py".format(root, tool_name)
dis_dir = "{}\\dist\\".format(root)
user_dist = "{}{}\\".format(dis_dir, tool_name)
app_cfg_dir = "{}\\config".format(root)
support_files = [os.path.join(root, 'config')]

app_cfg = Infra.read_json(app_cfg_dir, 'app_config.json')
version = app_cfg['version']
print(version)
Infra.remove_ff(dis_dir)
os.system("{} {} {}".format(builder, target, params))
sga_name = os.path.join(dis_dir, tool_name)
if "onefile" in params:
    sga_name = "{}{}".format(sga_name, '.exe')
    Infra.copy_ff(sga_name, user_dist)
for s_file in support_files:
    Infra.copy_ff(s_file, user_dist)
Infra.open_dir(dis_dir)
