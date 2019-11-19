from init.init_imports import Infra, DaPr, os


class GlobalConfig:

    def __init__(self):
        self.config_root = None
        self.server_config = None
        self.app_config_file_name = None
        self.app_config = None
        self.windows_event_config = None
        self.func_name_dict = None
        self.version = None
        self.group = None
        self.windows_update_out_date_day = 15
        self.curr_log_folder = None

    def set_value(self):
        self.config_root = DaPr.find_path_backward(os.getcwd(), "config")
        self.app_config_file_name = 'app_config.json'
        self.app_config = Infra.read_json(self.config_root,self.app_config_file_name)
        self.server_config = Infra.read_json(self.config_root, 'server_config.json')
        self.windows_event_config = self.server_config['windows_event_config']
        self.version = self.app_config['version']
        self.group = self.app_config['group']