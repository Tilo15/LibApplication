from LibApplication.Loop.GLib import GLibLoop
from LibApplication.Stock.Services.Application import ApplicationService

class Application:

    application_service = ApplicationService
    app_info = None

    def __init__(self):
        # Register the application
        self.application_service.register(self)

        # Prepare loop
        self.loop = GLibLoop()

        # Run preparations
        self.prepare()

        # Run startup tasks
        self.start()

        # When the loop starts, run ready
        self.loop.run(self.ready)

        # Start the loop
        self.loop.begin()


    def prepare(self):
        # Optionally Overridden
        pass

    def start(self):
        raise NotImplementedError

    def ready(self):
        # Optionally Overridden
        pass

    def close(self):
        # Optionally Overridden
        pass