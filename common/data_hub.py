class NdcHubStorage:

    def __init__(self):
        self.commands = None
        self.tasks = None
        self.groups = None
        self.accounts = None
        self.regx_rules = None
        self.total_task_num = None
        self.wait_task_num = None
        self.report_root = None


class SaltStorage:

    def __init__(self):
        self.sec = b'CiA6fx3T043gEkay37G8D200ZJ5WuKJdh9hbdvTRHL8='


NdcHub = NdcHubStorage()
Salt = SaltStorage()
