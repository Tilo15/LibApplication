

class DeferredConstructor:

    def __init__(self, constructor, *args):
        self.constructor = constructor
        self.args = args

    def construct(self):
        return self.constructor(*args)


def construct_all(obj):

    # Loop over each attribute
    for attr in dir(obj):

        # Get the item
        item = getattr(obj, attr, None)

        # It is a Deferred Constructor?
        if(isinstance(item, DeferredConstructor)):
            
            # Construct and set
            setattr(obj, attr, item.construct())
            
