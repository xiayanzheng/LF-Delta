import os

from init.init_imports import global_config as gc

files = os.listdir(gc.external_script_path)
print(files)
sub_files = os.listdir(os.path.join(gc.external_script_path, files[0]))
print(sub_files)
