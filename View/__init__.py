from LibApplication.Util import DeferredConstruction

from gi.repository import Gtk

import os
import sys

def View(path, root_id):

    # Create the decorator function
    def decorator(obj):
        # Extend the base object
        class ViewComponent(obj):
            
            # Constructor
            def __init__(self, *args, **kwargs):

                # Create a builder
                self._builder = Gtk.Builder()

                # Get the path of the current module
                module_path = os.path.abspath(sys.modules[obj.__module__].__file__)
                
                # Get the directory
                directiory = os.path.dirname(module_path)

                # Build the UI from XML
                self._builder.add_from_file(os.path.join(directiory, path))

                # Get the root object
                self._root = self._builder.get_object(root_id)

                # Run the base constructor
                obj.__init__(self, *args, **kwargs)

                # Run any defered constructors
                # DeferredConstruction.construct_all(self)

                # Connect signals
                self._builder.connect_signals(self)


            @staticmethod
            def bulk(arg_list):
                # New array
                views = []

                # Loop over each set of arguments
                for args in arg_list:
                    # Create the view
                    views.append(ViewComponent(*args))

                # Return the views
                return views

            def __del__(self):
                # Destroy
                self._root.destroy()


        return ViewComponent

    return decorator
