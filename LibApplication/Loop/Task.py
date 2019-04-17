import inspect
import rx


class Task:
    
    def __init__(self, call, *args):
        self.call = call
        self.args = args

    def run(self, observer: rx.Observer):
        # Is it a generator?
        if (inspect.isgeneratorfunction(self.call)):
            for item in self.call(*self.args):
                observer.on_next(item)

        else:
            observer.on_next(self.call(*self.args))

        observer.on_completed()