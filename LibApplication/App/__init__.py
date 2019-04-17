from LibApplication.Loop.GLib import GLibLoop

class Application:

    def __init__(self):
        # Prepare loop
        self.loop = GLibLoop()

        # Run any preparations
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