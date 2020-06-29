from init.init_imports import InfraX, DaPrX, os


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
        self.external_script_path = None
        self.external_script_result_path = None
        self.mode = None
        self.funcs = None

    def set_value(self):
        self.config_root = DaPrX.find_path_backward(os.getcwd(), "config")
        self.app_config_file_name = 'app_config.json'
        self.app_config = InfraX.read_json(self.config_root,self.app_config_file_name)
        self.server_config = InfraX.read_json(self.config_root, 'server_config.json')
        self.windows_event_config = self.server_config['windows_event_config']
        self.version = self.app_config['version']
        self.group = self.app_config['group']
        self.external_script_path = DaPrX.find_path_backward(os.getcwd(), "external_script")
        self.external_script_result_path = DaPrX.find_path_backward(os.getcwd(), "external_script_result")
        self.mode = self.app_config['mode']