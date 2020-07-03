import win32com.client


class WinUpdateInterface:

    def __init__(self):
        self.keeper = win32com.client.Dispatch('Microsoft.Update.Session')

        self.seeker = self.keeper.CreateUpdateSearcher()

        self.quaffle = win32com.client.Dispatch('Microsoft.Update.UpdateColl')

        self.bludger = win32com.client.Dispatch('Microsoft.Update.UpdateColl')

        # list of updates to be installed.
        self.bludger = win32com.client.Dispatch('Microsoft.Update.UpdateColl')

        self.auto_update = win32com.client.Dispatch('Microsoft.Update.AutoUpdate')

        # the object responsible for fetching the actual downloads.
        self.chaser = self.keeper.CreateUpdateDownloader()
        self.chaser.Updates = self.quaffle

        # the object responsible for the installing of the updates.
        self.beater = self.keeper.CreateUpdateInstaller()
        self.beater.Updates = self.bludger

    def search(self):
        seeker = self.keeper.CreateUpdateSearcher()
        uh = seeker.QueryHistory(0, 1000)
        print(uh)
        for his in uh:
            nh = his
            print(nh.UpdateIdentity.Date)
        # print(dir(dn))
        # print(dir(dn.get_LastInstallationSuccessDate()))

        # search_installed = seeker.Search('IsInstalled=1')
        # print(search_installed)
        # updates_installed = win32com.client.Dispatch("Microsoft.Update.UpdateColl")
        # for inst in search_installed.Updates:
        #     ids = ['Type','DeploymentAction','BrowseOnly','AutoSelectOnWebSites','UpdateID']
        #     print(inst.__dict__)


wu = WinUpdateInterface()
wu.search()
