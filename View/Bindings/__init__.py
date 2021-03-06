from LibApplication.Util.DeferredConstruction import DeferredConstructor
import weakref


class BaseBinding(object):
    
    def __init__(self, builder_id, attr):
        # GTK Builder Id
        self.ui_id = builder_id

        # Attribute to set on GTK component
        self.attribute = attr


    def get_component(self, instance):
        # ui_id can be a function for getting the widget
        if(callable(self.ui_id)):
            return self.ui_id(instance)

        # Get builder
        builder = getattr(instance, "_builder", None)

        # Error if no builder
        if(builder == None):
            raise TypeError("View bindings only work on classes decorated with a '@View' decorator.")

        # Get the GTK component
        return builder.get_object(self.ui_id)

    '''Given and object and attribute, determines if this binding type is valid'''
    @staticmethod
    def is_valid(self, target, **kwargs):
        raise NotImplementedError


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
        

# def FormattedBinding(builder_id, attr):

#     class BindingFormatter(Binding):

#         def __init__(self, func):
#             self.ui_id = builder_id
#             self.attribute = attr
#             self.func = func
#             self.values = weakref.WeakKeyDictionary()

#         def __get__(self, instance, owner):
#             # Return what was set, rather than the formatted value
#             if(instance in self.values):
#                 return self.values[instance]

#             return None

#         def __set__(self, instance, value):
#             # Format the value
#             formatted = self.func(instance, value)

#             # Set the value
#             Binding.__set__(self, instance, formatted)


#             # Save the value in case __get__ gets called
#             self.values[instance] = value

#     return BindingFormatter



# # TODO Image binding (Ie. From File (and perhaps from Pixbuf))
# class PixbufBinding(Binding):

#     def __init__(self, builder_id):
#         self.ui_id = builder_id
#         self.values = weakref.WeakKeyDictionary()

#     def __get__(self, instance, owner):
#         # Return what was set, rather than the formatted value
#         if(instance in self.values):
#             return self.values[instance]

#         return None

#     def __set__(self, instance, value):
#         # Get the GTK Image object
#         gtk_obj = Binding.get_component(self, instance)

#         # Set
#         gtk_obj.set_from_pixbuf(value)

#         # Save the value in case __get__ gets called
#         self.values[instance] = value

