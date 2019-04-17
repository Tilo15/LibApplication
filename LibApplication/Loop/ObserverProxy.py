import rx

class ObserverProxy(rx.Observer):

    def __init__(self, observer: rx.Observer, loop):
        self._observer = observer
        self._loop = loop

    def on_next(self, value):
        self._loop.run(self._observer.on_next, value)

    def on_completed(self):
        self._loop.run(self._observer.on_completed)

    def on_error(self, error):
        self._loop.run(self._observer.on_error, error)