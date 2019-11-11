from init.init_imports import InfraX, DaPr, os


class GlobalConfig:

    def __init__(self):
        self.config_root = None
        self.server_config = None
        self.windows_event_config = None
        self.func_name_dict = None

    def set_value(self):
        self.config_root = DaPr.find_path_backward(os.getcwd(), "config")
        self.server_config = InfraX.read_json(self.config_root, 'server_config.json')
        self.windows_event_config = self.server_config['windows_event_config']

    def set_func_name(self):
        func_name_dict = {
            'get_installed_win_updates':'Get Windows Installed Updates',
            'get_installed_software_list':'Get Installed Software List',
            'get_basic_info':'Get Basic Info',
            'get_disk_partitions':'Get Disk Info',
            'get_network_basic':'Get Network Basic',
            'get_event_log':'Get Event Log',
            'get_ping_result':'Get Ping Result',
            'get_summary':'Get Summary'
        }
        self.func_name_dict = func_name_dict