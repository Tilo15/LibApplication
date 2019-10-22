from LibApplication.Loop.ObserverProxy import ObserverProxy
from LibApplication.Loop.Service import LoopService

import rx

class Loop:

    loop_service = LoopService

    def add(self, task, reply_loop = None) -> rx.Observable:
        # If no reply loop was specified
        if(reply_loop == None):
            # Get current loop if possible
            reply_loop = self.loop_service.get_loop()

        # Create the observable function
        def on_subscribe(observer: rx.Observer):
            # Create an observer proxy
            proxy = ObserverProxy(observer, reply_loop)

            # Run the task with the observer proxy
            self.run(task.run, proxy)

        # Return the observable
        return rx.Observable.create(on_subscribe)


    def register(self):
        self.loop_service.register(self)

    def wait_for(self, observable: rx.Observable):
        # Error if not on this loop
        if(self != self.loop_service.get_loop()):
            raise Exception("Loop.wait_for can only be called from the thread that the loop is running on.")

        # Completed status
        completed = False

        # Observable value
        value = None

        # Callback for when our task is completed
        def callback(v):
            nonlocal completed
            nonlocal value
            completed = True
            value = v

        # Subscribe to the observable
        observable.subscribe(callback)

        # Keep doing things until we are done
        while not completed and self.is_alive():
            self.do_next()

        # Did it complete?
        if(not completed):
            raise Exception("Loop.wait_for was canceled as the loop has been stopped.")

        # Done, get the value
        return value



    def run(self, call, *args):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def begin(self):
        raise NotImplementedError

    def do_next(self):
        raise NotImplementedError

    def is_alive(self):
        raise NotImplementedError


