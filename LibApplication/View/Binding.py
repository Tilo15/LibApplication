from LibApplication.View.Bindings import BaseBinding
from LibApplication.View.Bindings.IconBinding import IconBinding
from LibApplication.View.Bindings.SpinnerBinding import SpinnerBinding

import weakref


BINDING_TYPES = [IconBinding, SpinnerBinding]

class Binding(BaseBinding):
    
    def __init__(self, builder_id, attr, **kwargs):
        # GTK Builder Id
        self.ui_id = builder_id

        # Attribute to set on GTK component
        self.attribute = attr

        # Additional arguments
        self.arguments = kwargs

        self.binding = None
        self.formatter = None
        self.values = weakref.WeakKeyDictionary()

    def setup(self, instance):
        # Get the component
        component = self.get_component(instance)

        # Determine the type of binding
        binding = BaseBinding
        for item in BINDING_TYPES:
            try:
                if(item.is_valid(component, self.attribute, **self.arguments)):
                    binding = item
                    break
            except:
                pass

        # Save the binding
        self.binding = binding(self.ui_id, self.attribute, **self.arguments)

        # Return the binding
        return self.binding

    def get_binding(self, instance):
        # Do we have a binding?
        if(self.binding != None):
            return self.binding

        # Setup the binding
        return self.setup(instance)


    def __get__(self, instance, owner):
        # Are we using a formatter function?
        if(self.formatter != None):
            # Do we have a value for this instance?
            if(instance in self.values):
                return self.values[instance]

            # Return None
            return None

        # Otherwise, use the underlying binding
        return self.get_binding(instance).__get__(instance, owner)
        

    def __set__(self, instance, value):
        # Hold the augmented value
        new_value = value

        # Are we using a formatter function?
        if(self.formatter != None):
            # Run the value through the formatter
            new_value = self.formatter(instance, value)

            # Update the value stored for this instance
            self.values[instance] = value

        # Set the value using the actual binding
        self.get_binding(instance).__set__(instance, new_value)


    def __call__(self, func):
        # This is decorating a formatter function
        if(callable(func)):
            self.formatter = func
            return self
        
        else:
            raise Exception("Bindings may only decorate formatter functions")
        