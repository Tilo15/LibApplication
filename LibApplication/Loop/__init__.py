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

            # Run the task wiht the observer proxy
            self.run(task.run, proxy)

        # Return the observable
        return rx.Observable.create(on_subscribe)


    def register(self):
        self.loop_service.register(self)

    def run(self, call, *args):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def begin(self):
        raise NotImplementedError

