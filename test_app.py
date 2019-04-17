from LibApplication.App import Application


from test import MyWindow

class TestApp(Application):

    def start(self):
        window = MyWindow()
        window.show()


TestApp()