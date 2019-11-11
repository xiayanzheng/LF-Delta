import os
from Delta.init.init_imports import InfraX

# os.chdir(os.getcwd)

builder = "E:\Resource\CodeOplex\Envs\LF-Nova\Scripts\pyinstaller.exe"
target = "E:\Resource\CodeOplex\LF-Cyber\Delta\infoCollector.py"
paramas = "--onefile"
dis_dir = "E:\Resource\CodeOplex\LF-Cyber\Delta\dist"
InfraX.remove_ff(dis_dir+"\\infoCollector")
os.system("{} {} {}".format(builder,target,paramas))
os.system("explorer.exe {}".format(dis_dir))