from init.init_imports import Infra, DaPr, os


class GlobalConfig:

    def __init__(self):
        self.config_root = None
        self.server_config = None
        self.app_config = None
        self.windows_event_config = None
        self.func_name_dict = None
        self.version = None

    def set_value(self):
        self.config_root = DaPr.find_path_backward(os.getcwd(), "config")
        self.app_config = Infra.read_json(self.config_root, 'app_config.json')
        self.server_config = Infra.read_json(self.config_root, 'server_config.json')
        self.windows_event_config = self.server_config['windows_event_config']
        self.func_name_dict = self.app_config['func_name_dict']
        self.version = self.app_config['version']
