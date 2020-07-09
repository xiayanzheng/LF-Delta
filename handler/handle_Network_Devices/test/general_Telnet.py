from init.init_imports import PrettyTable, Infra
from init.init_imports import TelnetConn as Telnet_conn


class TelnetSe(Telnet_conn):

    def __init__(self):
        self.user_groups = None
        self.user_tasks = None
        self.buffer = []
        self.debug = True

    def dump_to_file(self):
        # msg = self.tn.read_all().decode('ascii')
        msg = self.buffer
        fout = open('mylog.txt', 'w')
        for x in msg:
            if self.debug:
                print(type(x), x)
            fout.write("{}\n".format(x))
        fout.close()


if __name__ == '__main__':
    raw_cfg = Infra.read_json("..\\config\\", "network_device_config.json")

    tc = TelnetSe()
    tc.user_groups = raw_cfg['groups']
    tc.user_tasks = raw_cfg['tasks']
    tc.user_commands = raw_cfg['commands']
    tc.debug = False

    table = PrettyTable(["GroupID", "Group", "DeviceName", "IP"])
    selections, uuid = {}, 1
    for k, v in tc.user_groups.items():
        # table.add_row([k,])
        for k2, v2 in v.items():
            for x in v2.keys():
                GID, GNM = "", ""
                if uuid not in selections.keys() and k not in selections.values():
                    GID, GNM = uuid, k
                    selections[str(GID)] = GNM
                    uuid += 1
                table.add_row([GID, GNM, v2[x]["desc"], v2[x]["host"]])
    print(table)
    user_select = input("Please input [GroupID] to select group:")
    if user_select in selections.keys():
        selected = selections[user_select]
    for device in tc.user_groups[selected]['devices']:
        device_detail = tc.user_groups[selected]['devices'][device]
        tc.create_telnet_session(device_detail['host'], device_detail['port'])
        tasks = device_detail['device_tasks']
        for task in tasks:
            for cmd in tc.user_tasks[task]['commands']:
                cmd = tc.user_commands[cmd]
                print(cmd)
                # print("Doing>[Group:{}]-[Device:{}]-[IP:{}]-[Command:{}]"
                #       .format(selected,device_detail['desc'],device_detail['host']))
                tc.telnet_interface(**cmd)
    tc.dump_to_file()
