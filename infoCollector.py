from init.init_imports import Infra, os, socket, datetime, wmi_evt_qu, global_config
from handle_Server import server


def intro():
    print("Delta Version:{}".format(global_config.version))


def main():
    os.system("cls")
    intro()
    hostname = socket.getfqdn(socket.gethostname())
    if not os.path.exists(".\\Reports\\"):
        os.mkdir(".\\Reports\\")
    group_name = input("GroupName:")
    log_folder = "{}_{}".format(group_name,datetime.datetime.now().strftime('%Y-%m-%d'))
    log_path = '.\\Reports\\{}\\{}'.format(log_folder,hostname)
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    server.get_basic_info(log_path, 'host_basic_data.csv')
    server.get_disk_partitions(log_path, 'disk_info.csv')
    default_gateway = server.all_data['default_gateway']
    server.get_ping_result(default_gateway, log_path, 'ping_{}.txt'.format(default_gateway))
    server.get_installed_win_updates(log_path, 'installed_win_updates.csv')
    event_log_cfg = global_config.windows_event_config
    server.get_event_log(event_log_cfg, log_path, 'windows_event_log.csv')
    server.get_summary(log_path, 'Summary.csv')
    Infra.open_dir(log_path)
    os.system("pause")


main()
