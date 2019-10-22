from LibApplication.Service import Service

import threading

@Service
class LoopService:

    def __init__(self):
        self.loops = {}

    def register(self, loop):
        # Get current thread
        thread = threading.current_thread()

        # Save loop
        self.loops[thread] = loop

    def get_loop(self):
        # Get current thread
        thread = threading.current_thread()

        # Return loop
        return self.loops[thread]

    def shutdown(self):
        # Loop through each loop
        for loop in self.loops.values():
            # Tell it to stop
            loop.stop()
