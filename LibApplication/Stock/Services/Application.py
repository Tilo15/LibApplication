from LibApplication.Service import Service
from LibApplication.App.AppInfo import AppInfo

@Service
class ApplicationService:

    application = None
    namespace = None

    def register(self, application):
        self.application = application
        self.namesapce = application.app_info.namespace