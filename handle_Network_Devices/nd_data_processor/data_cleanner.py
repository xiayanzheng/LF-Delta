from handle_Network_Devices.nd_data_processor.common_process import CommonDataProcess


class DataCleaner(CommonDataProcess):

    def clean(self, cmd, data, regx_rule, cmd_index):
        r_data = None
        cmd_cfg = cmd_index[cmd]
        regx = regx_rule[cmd_cfg["rule"]]['rule']
        methods = regx_rule[cmd_cfg["rule"]]['method']
        try:
            if len(methods) != 0:
                for method in methods:
                    r_data = getattr(self, method)(regx, data)
            return r_data
        except Exception as e:
            print("[!][{}]Fail to exec regx rule,return raw data, Err-Msg:{}".format(cmd, e))
            return data
