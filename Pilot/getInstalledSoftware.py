from init.init_imports import winreg,Save


class Entry:

    def __init__(self):
        self.reg_path_uninstall = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        self.kav_install_path_a = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\UserData'
        self.total_installed_software_num = None
        self.installed_software = None

    def open_reg(self,reg_dir):
        return winreg.ConnectRegistry(None, reg_dir)

    def close_reg(self,reg_root):
        winreg.CloseKey(reg_root)

    def get_installed_software_list(self):
        reg_root = self.open_reg(winreg.HKEY_LOCAL_MACHINE)
        installed_soft64 = winreg.OpenKey(reg_root, self.reg_path_uninstall)
        self.total_installed_software_num = winreg.QueryInfoKey(installed_soft64)[0]
        for i in range(self.total_installed_software_num):
            # 3.穷举每个键，获取键名
            sub_key_name = winreg.EnumKey(installed_soft64, i)
            sub_dir_2 = r'%s\%s' % (self.reg_path_uninstall, sub_key_name)
            # 4.根据获取的键名拼接之前的路径作为参数，获取当前键下所属键的控制
            key_handle_2 = winreg.OpenKey(reg_root, sub_dir_2)
            count2 = winreg.QueryInfoKey(key_handle_2)[1]
            temp = {}
            for j in range(count2):
                # 5.穷举每个键，获取键名、键值以及数据类型
                name, value, count_type = winreg.EnumValue(key_handle_2, j)
                if name == 'DisplayName':
                    temp['Name'] = value
                elif name == 'DisplayVersion':
                    temp['Version'] = value
                keys = list(temp.keys())
                if 'Name' in keys and 'Version' in keys:
                    self.installed_software.append(temp)
                    temp = {}
            winreg.CloseKey(key_handle_2)  # 读写操作结束后关闭键
        winreg.CloseKey(installed_soft64)
        self.close_reg(reg_root)

    def save_install_software_list(self,log_path, log_file):
        data = self.installed_software
        title = list(data[0].keys())
        Save.toCSV(log_path, log_file, title, data)

    def get_kav_version(self):
        reg_root = self.open_reg(winreg.HKEY_LOCAL_MACHINE)
        kav_install_path_a = winreg.OpenKey(reg_root, self.kav_install_path_a)
        kav_install_path_a_reco_num = winreg.QueryInfoKey(kav_install_path_a)[0]
        for i in range(kav_install_path_a_reco_num):
            sub_key_name = winreg.EnumKey(kav_install_path_a, i)
            print(sub_key_name)
            sub_dir_2 = r'%s\%s' % (self.kav_install_path_a, sub_key_name)
            print(sub_dir_2)
            # 4.根据获取的键名拼接之前的路径作为参数，获取当前键下所属键的控制
            key_handle_2 = winreg.OpenKey(reg_root, sub_dir_2)
            count2 = winreg.QueryInfoKey(key_handle_2)[0]
            print(count2)
            for j in range(count2):
                # 5.穷举每个键，获取键名、键值以及数据类型
                name, value, count_type = winreg.EnumValue(key_handle_2, j)
                print(name, value, count_type)


s1 = Entry()
s1.get_kav_version()
