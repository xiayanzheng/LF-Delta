from init.init_imports import Infra, Save, DaPr, Numbers, wmi_evt_qu, global_config, datetime
from init.init_imports import psutil, socket, platform, wmi, subprocess, netifaces, show_status, winreg, os


class Entry:

    def __init__(self):
        self.all_data = None
        self.wmi_connector = wmi.WMI()

    @show_status
    def get_basic_info(self, log_path, log_file, debug=False):
        def get_cpu_name():
            wmi_data = {}
            for cpu in self.wmi_connector.Win32_Processor():
                wmi_data['cpu_name'] = cpu.Name
            return wmi_data

        def get_hardware_info():
            # os.system("wmic qfe list")
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
                "cpu_name": get_cpu_name()['cpu_name'],
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
            if not debug:
                Save.to_csv(log_path, log_file, header, data)
            self.all_data = info

        get_hardware_info()

    @show_status
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
                Save.to_csv(log_path, log_file, headers=head, data=disk_info)
                for k, v in disk.items():
                    if k in ['total_gb', 'used_gb', 'free_gb', 'percentage_of_use']:
                        sk = "{}_{}_{}".format(disk["disk"], disk["fstype"], k)
                        sv = v
                        self.all_data[sk] = sv
            except:
                pass

    @show_status
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

    @show_status
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
        Save.to_csv(log_path, log_file, key, base)

    @show_status
    def get_ping_result(self, ip, log_path, log_file):
        cmd = "ping {}".format(ip)
        p = subprocess.Popen(cmd,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)
        data = p.stdout.read().decode('gb2312')
        Save.to_txt(log_path, log_file, data)

    @show_status
    def get_license_key(self, log_path, log_file, debug=False):
        all_license = []

        def windows():
            license_ = self.wmi_connector.query("select * from SoftwareLicensingService")
            for lic in license_:
                buck = {"name": "Microsoft Windows "}
                if hasattr(lic, 'OA3xOriginalProductKey'):
                    windows_license = getattr(lic, 'OA3xOriginalProductKey')
                    if hasattr(lic, 'Version'):
                        buck["name"] = buck['name'] + getattr(lic, 'Version')
                        buck["license"] = windows_license
                    else:
                        buck["license"] = windows_license
                else:
                    buck["license"] = None
                all_license.append(buck)

        def save():
            keys = list(all_license[0].keys())
            Save.to_csv(log_path, log_file, keys, all_license)

        windows()
        if not debug:
            save()

    @show_status
    def get_summary(self, log_path, log_file):
        headers = ['item', self.all_data['pc_name']]
        data_f = []
        for k, v in self.all_data.items():
            data_f.append({headers[0]: k, headers[1]: v})
        Save.to_csv(log_path, log_file, headers, data_f)

    @show_status
    def get_installed_software(self, log_path, log_file):
        keys = ['Caption', 'Version', 'InstallDate', 'InstallLocation']
        installed = []
        win32_product = self.wmi_connector.query("Select * from Win32_Product")
        for x in win32_product:
            installed_temp = {}
            for key in keys:
                if hasattr(x, key):
                    installed_temp[key] = getattr(x, key)
                else:
                    installed_temp[key] = None
            installed.append(installed_temp)
        keys = list(installed[0].keys())
        Save.to_csv(log_path, log_file, keys, installed)

    @show_status
    def get_windows_update_status(self, log_path, log_file, debug=False):

        def get_installed_win_updates(log_path_c, log_file_c, raw, debug_c):
            all_data = []
            for x in raw:
                keys = list(x.properties.keys())
                unit = {}
                for key in keys:
                    if hasattr(x, key):
                        unit[key] = getattr(x, key)
                all_data.append(unit)
            n_key = list(all_data[0].keys())
            if not debug_c:
                Save.to_csv(log_path_c, log_file_c, n_key, all_data)
            return all_data

        def get_windows_date():
            installed_on_flag = 'InstalledOn'
            raw = self.wmi_connector.query("SELECT * from Win32_QuickFixEngineering")
            windows_update_info = get_installed_win_updates(log_path, log_file, raw, debug)
            last_update_install_time = None
            for record in windows_update_info:
                if installed_on_flag in record:
                    installed_on_time = datetime.datetime.strptime(record[installed_on_flag], '%m/%d/%Y')
                    if last_update_install_time is None:
                        last_update_install_time = installed_on_time
                    if installed_on_time > last_update_install_time:
                        last_update_install_time = installed_on_time
            diff = datetime.datetime.now() - last_update_install_time
            out_date_day = global_config.windows_update_out_date_day
            if not debug:
                self.all_data['is_windows_update_outdated'] = diff.days > out_date_day

        get_windows_date()

    @show_status
    def get_kav_update_status(self):
        try:
            kav_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\KasperskyLab\Binaries\KES_X86")
            avp_com = "avp.com"
            kav_install_path, _ = winreg.QueryValueEx(kav_key, avp_com)
            kav_install_path = kav_install_path[0:len(kav_install_path) - len(avp_com)]
            curr_dir = os.getcwd()
            os.chdir(kav_install_path)
            kav_version_query = "{} {} {}".format(avp_com, "STATISTICS", "Updater")
            raw = Infra.cmd_con_lite(kav_version_query)
            os.chdir(curr_dir)
            valid = ["Start", "Finish"]
            for line in raw:
                for i in range(len(valid)):
                    key = valid[i]
                    if key in line:
                        self.all_data["kav_update_{}_time".format(key).lower()] = DaPr.match_datetime_from_str(line)
        except FileNotFoundError:
            pass
