from LibApplication.Loop import Loop
from LibApplication.Loop.Service import LoopService

import rx

class Push:

    loop_service = LoopService

    def __init__(self):
        # Hold observer loop pairs
        self.observers = set()

        # Define the subscribe function
        def on_subscribe(observer):
            # Get the subscriber's loop
            subscriber_loop = self.loop_service.get_loop()

            # Add the observer loop pair
            self.observers.add((observer, subscriber_loop))

        # Create the underlying observable
        self.observable = rx.Observable.create(on_subscribe)

    def push(self, obj):
        # Queue to each observer
        for observer, loop in self.observers:
            loop.run(observer.on_next, obj)

    def subscribe(self, *args, **kwargs):
        self.observable.subscribe(*args, **kwargs)
