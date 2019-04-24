import weakref
import rx


class Event(object):

    def __init__(self, func):
        self.func = func
        self.subjects = weakref.WeakKeyDictionary()

    def __get__(self, instance, owner):
        # Create subject for this instance if it doesn't exist
        if(instance not in self.subjects):
            self.subjects[instance] = rx.subjects.Subject()

        class EventProxy(object):
            def __call__(*args):
                result = self.func(instance)
                self.subjects[instance].on_next(result)

            def __getattribute__(proxy, name):
                return self.subjects[instance].__getattribute__(name)

        return EventProxy()
