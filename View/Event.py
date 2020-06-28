import weakref
import rx
import inspect

class Event(object):

    def __init__(self, func = lambda x, y: y):
        self.func = func
        self.subjects = weakref.WeakKeyDictionary()

    def __get__(self, instance, owner):
        # Create subject for this instance if it doesn't exist
        if(instance not in self.subjects):
            self.subjects[instance] = rx.subjects.Subject()

        class EventProxy(object):
            def __call__(*args):
                sig = inspect.signature(self.func)
                # Only pass as many as the function can take
                result = self.func(instance, *args[1:len(sig.parameters)])
                self.subjects[instance].on_next(result)

            def __getattribute__(proxy, name):
                return self.subjects[instance].__getattribute__(name)

        return EventProxy()
