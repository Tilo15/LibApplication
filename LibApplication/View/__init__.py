from LibApplication.Util import DeferredConstruction

from gi.repository import Gtk

def View(path, root_id):

    # Create the decorator function
    def decorator(obj):
        # Extend the base object
        class ViewComponent(obj):
            
            # Constructor
            def __init__(self, *args):

                # Create a builder
                self._builder = Gtk.Builder()

                # Build the UI from XML
                self._builder.add_from_file(path)

                # Get the root object
                self._root = self._builder.get_object(root_id)

                # Run the base constructor
                obj.__init__(self, *args)

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


        return ViewComponent

    return decorator


