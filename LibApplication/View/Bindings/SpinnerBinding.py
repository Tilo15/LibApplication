from LibApplication.View.Bindings import BaseBinding
from gi.repository.Gtk import Spinner
import weakref

class SpinnerBinding(BaseBinding):
    def __init__(self, builder_id, attribute):
        self.ui_id = builder_id
        self.values = weakref.WeakKeyDictionary()


    @staticmethod
    def is_valid(obj, attr, **kwargs):
        return isinstance(obj, Spinner) and attr == "active"


    def __get__(self, instance, owner):
        # Return what was set, rather than the formatted value
        if(instance in self.values):
            return self.values[instance]

        return None

    def __set__(self, instance, value):
        # Get the GTK Image object
        gtk_obj = self.get_component(instance)

        if(value):
            gtk_obj.start()
        else:
            gtk_obj.stop()

        # Save the value in case __get__ gets called
        self.values[instance] = value