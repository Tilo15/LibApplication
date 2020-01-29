from LibApplication.Service import Service
from LibApplication.App.AppInfo import AppInfo
from LibApplication.Loop.Service import LoopService

import os

@Service
class ApplicationService:

    loop_service = LoopService

    def register(self, application):
        self.application = application
        self.namespace = application.app_info.namespace

    def __init__(self):
        self.application = None
        self.namespace= None
        self.windows = set()

    def add_window(self, window_view):
        # Add the window to the set
        self.windows.add(window_view)

        # Attach an event for removing the window
        window_view._root.connect("hide", lambda x: self.remove_window(window_view))

    def remove_window(self, window_view):
        # Remove the window from the set
        self.windows.remove(window_view)

        # If there are no more windows open, call the application's close method
        if(len(self.windows) == 0):
            result = self.application.close()

            # If the function returned None or True, close the application
            if(result == None or result == True):
                self.loop_service.shutdown()

    @property
    def data_path(self):
        path = "todo_move_me_{0}".format(self.namespace)

        if(not os.path.exists(path)):
            os.mkdir(path)

        return path

