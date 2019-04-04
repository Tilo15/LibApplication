from LibApplication.Util.DeferredConstruction import DeferredConstructor

class Binding(object):
    
    def __init__(self, builder_id, attr):
        # Save the initial value
        # self.inital_value = initial_value

        # GTK Builder Id
        self.ui_id = builder_id

        # Attribute to set on GTK component
        self.attribute = attr


    def get_component(self, instance):
        # Get builder
        builder = getattr(instance, "_builder", None)

        # Error if no builder
        if(builder == None):
            raise TypeError("View bindings only work on classes decorated with a '@View' decorator.")

        # Get the GTK component
        return builder.get_object(self.ui_id)


    def __get__(self, instance, owner):
        # Get the GTK component object
        gtk_obj = self.get_component(instance)

        # Get the getter function
        get = getattr(gtk_obj, "get_%s" % self.attribute, None)

        # Make sure result is callable
        if(not callable(get)):
            raise TypeError("No '%s' get method on a '%s'" % (self.attribute, type(gtk_obj).__name__))

        # Return the value
        return get()


    def __set__(self, instance, value):
        # Get the GTK component object
        gtk_obj = self.get_component(instance)

        # Get the setter function
        setf = getattr(gtk_obj, "set_%s" % self.attribute, None)

        # Make sure result is callable
        if(not callable(setf)):
            raise TypeError("No '%s' set method on a '%s'" % (self.attribute, type(gtk_obj).__name__))

        # Set it
        setf(value)
        
