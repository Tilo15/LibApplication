from LibApplication.App import Application
from LibApplication.App.AppInfo import AppInfo

from test import MyWindow

class TestApp(Application):

    app_info = AppInfo("com.pcthingz.test", 0.1)

    def start(self):
        window = MyWindow()
        window.show()


TestApp()