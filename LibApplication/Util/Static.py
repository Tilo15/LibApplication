
def WithReferenceOwner(obj):
    '''Wrapper around an object that injects the instance that the object was retreived from into every function call of the class'''
    class ReferenceOwned(obj):
        def __init__(self, *args):
            # Construct the object
            self.obj = obj(*args)

        def __get__(self, instance, owner):
            return ClassWithInstance(self.obj, instance)

    return ReferenceOwned


class ClassWithInstance(object):

    def __init__(self, obj, instance):
        # Construct object
        base = super()

        # Set "obj" and "instance" attributes
        base.__setattr__("obj", obj)
        base.__setattr__("instance", instance)


    def __getattribute__(self, attr):
        # Get the base object
        base = super()

        # Get "obj" and "instance" attributes
        obj = base.__getattribute__("obj")
        instance = base.__getattribute__("instance")

        # Get the item from the object
        item = getattr(obj, attr)

        # If the item is callable
        if(callable(item)):
            # Wrap the call 
            def wrapper(*args):
                # Get the original class of the object, and statically call the desired function
                # setting self to this class - allowing subsequent calls to also contain the instance param
                return getattr(type(obj), attr)(self, instance, *args)

            return wrapper

        return item

    def __setattr__(self, attr, value):
        obj = super().base.__getattr__("obj")
        setattr(obj, attr, value)
