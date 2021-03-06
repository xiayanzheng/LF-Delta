from init.init_imports import InfraX, os, socket, datetime, prettytable
from init.init_imports import global_config as gc
from handle_server import server
from handle_report import mergeReports


def intro():
    os.system("cls")
    print("Delta Version:{}".format(gc.version))


def add_group():
    new_group_name = str(input("Pls input a new group name："))
    new_group_list = gc.app_config['group']
    if new_group_name in new_group_list:
        print("Group Name exists")
        select_group()
    new_group_list.append(new_group_name)
    gc.app_config['group'] = new_group_list
    InfraX.write_json(gc.config_root, gc.app_config_file_name, gc.app_config)
    gc.group = gc.app_config['group']
    select_group()


def select_group():
    intro()
    group_list = gc.group
    new_group_dict = {}
    pt = prettytable.PrettyTable()
    pt.field_names = ['No.', 'GroupName']
    for i in range(len(group_list)):
        no = str(i)
        name = group_list[i]
        pt.add_row([no, name])
        new_group_dict[no] = group_list[i]
    print(pt)
    info = "Please select a number from [No]\nif group name is not in this table pls input [a] to add a group："
    user_selected = input(info)
    if user_selected in ['a', 'A']:
        add_group()
    if user_selected in list(new_group_dict.keys()):
        selected_group = new_group_dict[str(user_selected)]
        return selected_group
    else:
        print("Group not exits")
        select_group()


def get_server_data(log_path):
    server.get_basic_info(log_path, 'host_basic_data.csv')
    server.get_kav_update_status()
    server.get_disk_partitions(log_path, 'disk_info.csv')
    server.get_license_key(log_path, 'license.csv')
    server.get_installed_software(log_path, 'installed_software.csv')
    default_gateway = server.all_data['default_gateway']
    server.get_ping_result(default_gateway, log_path, 'ping_{}.txt'.format(default_gateway))
    server.get_windows_update_status(log_path, 'installed_win_updates.csv')
    event_log_cfg = gc.windows_event_config
    server.get_event_log(event_log_cfg, log_path, 'windows_event_log.csv')
    server.get_summary(log_path, 'summary.csv')


def set_path_and_select_group(group_name):
    hostname = socket.getfqdn(socket.gethostname())
    if not os.path.exists(".\\Reports\\"):
        os.mkdir(".\\Reports\\")
    log_folder = "{}_{}".format(group_name, datetime.datetime.now().strftime('%Y-%m-%d'))
    gc.curr_log_folder = log_folder
    log_path = '.\\Reports\\{}\\{}'.format(log_folder, hostname)
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    return log_path, log_folder


def merge_reports(group_name):
    return mergeReports.merge(group_name)


def main():
    # log_path, log_folder = set_path_and_select_group("SMBC")
    # get_server_data(log_path)
    group_name = select_group()
    msg = "input [1] for get server status\ninput [2] for merge report\ninput [3] for reselect："
    selected_function = int(input(msg))
    if selected_function in [1, 2]:
        if selected_function == 1:
            log_path, log_folder = set_path_and_select_group(group_name)
            get_server_data(log_path)
            InfraX.open_dir(log_path)
        elif selected_function == 2:
            output_path, output_file = merge_reports(group_name)
            InfraX.open_dir(output_path)
        elif selected_function == 3:
            main()
        os.system("pause")
    else:
        print("invalid input")
        main()


main()

