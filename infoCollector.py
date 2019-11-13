from init.init_imports import Infra, os, socket, datetime, global_config, prettytable
from handle_Server import server
from handel_report import mergeReports


def intro():
    os.system("cls")
    print("Delta Version:{}".format(global_config.version))


def add_group():
    new_group_name = str(input("Pls input a new group name："))
    new_group_list = global_config.app_config['group']
    if new_group_name in new_group_list:
        print("Group Name exists")
        select_group()
    new_group_list.append(new_group_name)
    global_config.app_config['group'] = new_group_list
    Infra.write_json(global_config.config_root, global_config.app_config_file_name, global_config.app_config)
    select_group()


def select_group():
    intro()
    group_list = global_config.group
    new_group_list = {}
    pt = prettytable.PrettyTable()
    pt.field_names = ['No.', 'GroupName']
    for i in range(len(group_list)):
        no = str(i)
        name = group_list[i]
        pt.add_row([no, name])
        new_group_list[no] = group_list[i]
    print(pt)
    info = "Please select a number from No \nif group name is not in this table pls input a to add a group："
    user_selected = input(info)
    if user_selected in ['a', 'A']:
        add_group()
    if user_selected in list(new_group_list.keys()):
        selected_group = new_group_list[str(user_selected)]
        return selected_group
    else:
        print("Group not exits")
        select_group()


def get_server_data(log_path):
    server.get_basic_info(log_path, 'host_basic_data.csv')
    server.get_disk_partitions(log_path, 'disk_info.csv')
    default_gateway = server.all_data['default_gateway']
    server.get_ping_result(default_gateway, log_path, 'ping_{}.txt'.format(default_gateway))
    server.get_installed_win_updates(log_path, 'installed_win_updates.csv')
    event_log_cfg = global_config.windows_event_config
    server.get_event_log(event_log_cfg, log_path, 'windows_event_log.csv')
    server.get_summary(log_path, 'Summary.csv')


def set_path_and_select_group():
    hostname = socket.getfqdn(socket.gethostname())
    if not os.path.exists(".\\Reports\\"):
        os.mkdir(".\\Reports\\")
    group_name = select_group()
    log_folder = "{}_{}".format(group_name, datetime.datetime.now().strftime('%Y-%m-%d'))
    log_path = '.\\Reports\\{}\\{}'.format(log_folder, hostname)
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    return log_path, log_folder, group_name


def merge_reports(group_name):
    mergeReports.merge(group_name)


def main():
    log_path, log_folder, group_name = set_path_and_select_group()
    msg = "input [1] for get server status\ninput [2] for merge report\ninput [3] for reselect："
    select_function = int(input(msg))
    if select_function in [1, 2]:
        if select_function == 1:
            get_server_data(log_path)
        elif select_function == 2:
            merge_reports(group_name)
        elif select_function == 3:
            main()
        Infra.open_dir(log_path)
        os.system("pause")
    else:
        print("invalid input")
        main()


main()
