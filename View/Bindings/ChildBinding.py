from LibApplication.View.Bindings import BaseBinding
from gi.repository.Gtk import Image
import weakref

class ChildBinding(BaseBinding):

    def __init__(self, builder_id, attribute, size):
        self.ui_id = builder_id
        self.size = size
        self.values = weakref.WeakKeyDictionary()


    @staticmethod
    def is_valid(obj, attribute, **kwargs):
        return "child" in attribute


    def __get__(self, instance, owner):
        # Return what was set, rather than the formatted value
        if(instance in self.values):
            return self.values[instance]

        return None

    def __set__(self, instance, value):
        # Get the GTK Image object
        gtk_obj = self.get_component(instance)

        # Set
        super().__set__(instance, value._root)

        # Save the value in case __get__ gets called
        self.values[instance] = value