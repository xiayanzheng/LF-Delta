from init.init_imports import Infra, Save, DaPr, Numbers, wmi_evt_qu
from init.init_imports import winreg, psutil, socket, platform, wmi, subprocess, netifaces, show_status


class Entry:

    def __init__(self):
        self.all_data = None

    @show_status()
    def get_installed_win_updates(self, log_path, log_file):
        raw = Infra.cmd_con_lite("wmic qfe list")
        # print(raw)
        processed = []
        for line in raw:
            split_line = line.split('  ')
            inner = []
            for g in split_line:
                if g != '':
                    inner.append(g)
            if len(inner) != 0:
                processed.append(inner)
        key = processed[0]
        processed.pop(0)
        result = []
        for inner in processed:
            merged = DaPr.convert_two_lists_to_dict(key, inner)
            result.append(merged)
        # print(result)
        Save.toCSV(log_path, log_file, key, result)

    @show_status()
    def get_installed_software_list(self):
        regRoot = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        subDir = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        installed_soft64 = winreg.OpenKey(regRoot, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
        count = winreg.QueryInfoKey(installed_soft64)[0]
        print(count)
        for i in range(count):
            # 3.穷举每个键，获取键名
            subKeyName = winreg.EnumKey(installed_soft64, i)
            subDir_2 = r'%s\%s' % (subDir, subKeyName)
            # 4.根据获取的键名拼接之前的路径作为参数，获取当前键下所属键的控制
            keyHandle_2 = winreg.OpenKey(regRoot, subDir_2)
            count2 = winreg.QueryInfoKey(keyHandle_2)[1]
            for j in range(count2):
                # 5.穷举每个键，获取键名、键值以及数据类型
                name, value, type = winreg.EnumValue(keyHandle_2, j)
                # print("name:{},value：{}，Type：{}".format(name,value,type))
                ss = {}
                if name == 'DisplayName':
                    ss['name'] = value
                elif name == 'DisplayVersion':
                    ss['Version'] = value
                if ss:
                    print(ss)
                # if ('ProfileImagePath' in name and 'Users' in value):
                #     print(value)
            winreg.CloseKey(keyHandle_2)  # 读写操作结束后关闭键

        winreg.CloseKey(installed_soft64)
        winreg.CloseKey(regRoot)

    @show_status()
    def get_basic_info(self, log_path, log_file):
        # os.system("wmic qfe list")
        wmi_data = self.wmi_con()
        net_io = psutil.net_io_counters()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        info = {
            "pc_name": socket.getfqdn(socket.gethostname()),
            "os_version": platform.platform(),
            "ip_addr": s.getsockname()[0],
            "mac": str.upper(Infra.get_mac_address()),
            "default_gateway": netifaces.gateways()['default'][netifaces.AF_INET][0],
            "architecture": platform.architecture()[0],
            "cpu_name": wmi_data['cpu_name'],
            "cpu_family": platform.processor(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "cpu_count": psutil.cpu_count(),
            "process_count": len(psutil.pids()),
            "memory_used_percent": psutil.virtual_memory().percent,
            "memory_total_GB": Numbers.byte_to_gb(psutil.virtual_memory().total, 2),
            "memory_available_GB": Numbers.byte_to_gb(psutil.virtual_memory().available, 2),
            "memory_used_GB": Numbers.byte_to_gb(psutil.virtual_memory().used, 2),
            "memory_free_GB": Numbers.byte_to_gb(psutil.virtual_memory().free, 2),
            "network_io_sent_GB": Numbers.byte_to_gb(net_io[0], 2),
            "network_io_recv_GB": Numbers.byte_to_gb(net_io[1], 2),
            "network_io_packets_sent": net_io[2],
            "network_io_packets_recv": net_io[3],
        }
        header = ['item', 'data']
        data = []
        for k, v in info.items():
            data.append({'item': k, 'data': v})
        Save.toCSV(log_path, log_file, header, data)
        self.all_data = info

    @show_status()
    def get_disk_partitions(self, log_path, log_file):
        info = {
            "disk_partitions": psutil.disk_partitions(),
            "disk_info": [],
        }
        for x in info['disk_partitions']:
            try:
                num_fmt = "{}"
                disk_usage = psutil.disk_usage(x.mountpoint)
                disk = {}
                disk["disk"] = x.mountpoint
                disk["fstype"] = x.fstype
                disk["total_gb"] = num_fmt.format(Numbers.byte_to_gb(disk_usage.total))
                disk["used_gb"] = num_fmt.format(Numbers.byte_to_gb(disk_usage.used))
                disk["free_gb"] = num_fmt.format(Numbers.byte_to_gb(disk_usage.free))
                disk["percentage_of_use"] = disk_usage.percent
                info["disk_info"].append(disk)
                disk_info = info['disk_info']
                head = list(disk_info[0].keys())
                Save.toCSV(log_path, log_file, headers=head, data=disk_info)
                for k, v in disk.items():
                    if k in ['total_gb', 'used_gb', 'free_gb', 'percentage_of_use']:
                        sk = "{}_{}_{}".format(disk["disk"], disk["fstype"], k)
                        sv = v
                        self.all_data[sk] = sv
            except:
                pass

    @show_status()
    def get_network_basic(self):
        fi_data = {}

        for k, v in psutil.net_if_stats().items():
            re = {"isup": v[0], "speed": v[2], 'mtu': v[3]}
            fi_data[k] = re

        for k, v in psutil.net_if_addrs().items():
            fi_data[k]['mac'] = v[0][1]
            fi_data[k]['ipv4'] = v[1][1]
            fi_data[k]['mask'] = v[1][2]

        print(fi_data)

    @show_status()
    def get_event_log(self, cfg_set, log_path, log_file):
        wmi_evt_qu.disable_insertion_strings = False
        base = []
        for cfg in cfg_set:
            data = wmi_evt_qu.get_log(cfg, cfg['start_date'], cfg['end_date'])
            base.extend(data)

        for event in base:
            evt_type = "Event_{}".format(event['Type'])
            if evt_type not in self.all_data.keys():
                self.all_data[evt_type] = 1
            else:
                self.all_data[evt_type] += 1
        if len(base) != 0:
            key = list(base[0].keys())
        else:
            key = ['result']
            base = [{'result': 'No data'}]
        Save.toCSV(log_path, log_file, key, base)

    @show_status()
    def get_ping_result(self, ip, log_path, log_file):
        cmd = "ping {}".format(ip)
        p = subprocess.Popen(cmd,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)
        # for line in iter(p.stdout.readline, b''):
        #     de_line = line.decode('gb2312')
        # p.stdout.close()
        # p.wait()
        data = p.stdout.read().decode('gb2312')
        Save.toTXT(log_path, log_file, data)

    @show_status()
    def get_summary(self, log_path, log_file):
        headers = ['item', self.all_data['pc_name']]
        data_f = []
        for k, v in self.all_data.items():
            data_f.append({headers[0]: k, headers[1]: v})
        Save.toCSV(log_path, log_file, headers, data_f)

    def wmi_con(self):
        wmi_data = {}
        w = wmi.WMI()  # can put other server here if needed

        for cpu in w.Win32_Processor():
            wmi_data['cpu_name'] = cpu.Name

        times = DaPr.string_to_datetime('2019/10/12')

        # for log in w.Win32_NTLogEvent(EventType=2, Logfile="System"):
        #     print(log)

        # print("________________name_space____________________")
        # for process in w.Win32_Process():
        #     print(process.ProcessId, process.Name)
        # print("________________services____________________")
        # for service in w.Win32_Service():
        #     print(service.ProcessId, service.Name)
        return wmi_data
