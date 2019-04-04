
def WithReferenceOwner(obj):
    '''Wrapper around an object that injects the instance that the object was retreived from into every function call of the class'''
    class ReferenceOwned(obj):
        def __init__(*args):
            # Construct the object
            obj.__init__(*args)

        def __get__(self, instance, owner):
            base = super().__get__(instance, owner)
            return ClassWithInstance(base, instance)

    return ReferenceOwned


class ClassWithInstance(object):

    def __init__(self, obj, instance):
        # Construct object
        base = super()

        # Set "obj" and "instance" attributes
        base.__setattr__("obj", obj)
        base.__setattr__("instance", instance)


    def __getattr__(self, attr):
        # Get the item from the object
        item = getattr(self.obj, attr)

        # If the item is callable
        if(callable(item)):
            # Wrap the call 
            def wrapper(*args):
                return item(self.instance, *args)

            return wrapper

        return item

    def __setattr__(self, attr, value):
        setattr(self.obj, attr, value)
