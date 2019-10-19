import inspect
import rx


class Task:
    
    def __init__(self, call, *args, **kwargs):
        self.call = call
        self.args = args
        self.kwargs = kwargs

    def run(self, observer: rx.Observer):
        # Is it a generator?
        try:
            if (inspect.isgeneratorfunction(self.call)):
                for item in self.call(*self.args, **self.kwargs):
                    observer.on_next(item)

            else:
                observer.on_next(self.call(*self.args, **self.kwargs))

        except Exception as e:
            observer.on_error(e)

        observer.on_completed()