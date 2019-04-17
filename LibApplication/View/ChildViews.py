from LibApplication.View import View

from gi.repository import Gtk


class ChildViews(object):
    
    def __init__(self, ui_id):
        self.ui_id = ui_id
        self.outlets = {}
        self.view_mapping = {}


    def __set__(self, instance, values):
        self.set_views(values, instance)


    def set_views(self, views, instance):
        # Get builder
        builder = getattr(instance, "_builder", None)

        # Error if no builder
        if(builder == None):
            raise TypeError("Outlets can only exist on classes with a '@View' decorator.")

        # Get the outlet
        outlet = builder.get_object(self.ui_id)

        # Remove children
        children = outlet.get_children()
        for child in children:
            outlet.remove(child)

        # Add in the views
        for view in views:
            # Make sure view GTK component not already part of something else
            parent = view._root.get_parent()

            if(parent != None):
                parent.remove(view._root)
            
            while Gtk.events_pending():
                Gtk.main_iteration_do(True)

            outlet.add(view._root)
            view._root.show_all()


        # Save views
        self.outlets[instance] = outlet

        # Save a map of root objects to views
        self.view_mapping[instance] = {}
        for view in views:
            self.view_mapping[instance][view._root] = view


    def __get__(self, instance, owner):
        if(instance in self.view_mapping):
            return ChildViewsOutlet(self, instance)

        return None


class ChildViewsOutlet(object):

    def __init__(self, views, instance):
        super().__setattr__("_views", views)
        super().__setattr__("_instance", instance)


    def _handle_get(self, widget):
        # If the result is a GTK object
        if(isinstance(widget, Gtk.Widget)):
            # Check if the widget is in the view mapping
            if(widget in self._views.view_mapping[self._instance]):
                return self._views.view_mapping[self._instance][widget]

            # Unwrap until we find the right one
            return self._handle_get(widget.get_child())

        return widget


    def _handle_set(self, view):
        # If the item is a view
        if(hasattr(view, "_root")):
            # Make sure it's in the map
            self._views.view_mapping[self._instance][view._root] = view

            # Return the nearest child to our outlet
            return self._find_nearest_child(view._root, self._views.outlets[self._instance])

        return view


    def _find_nearest_child(self, item, ancestor):
        # Is the parent out outlet?
        parent = item.get_parent()
        if(parent != ancestor):
            return self._find_nearest_child(parent, ancestor)

        return item



    def __getattr__(self, attr):
        # Get the outlet
        outlet = self._views.outlets[self._instance]

        # Try and get the getter
        try:
            get = getattr(outlet, "get_%s" % attr)

        except:
            # Get the attribute
            value = getattr(outlet, attr)

            # If it's callable, wrap it up
            if(callable(value)):
                def wrapper(*args):
                    clean_args = [self._handle_set(x) for x in args]
                    result = value(*clean_args)
                    
                    # If the result is a list
                    if(isinstance(result, list) and len(result) > 0):
                        # Return handled objects
                        return [self._handle_get(x) for x in result]

                    return self._handle_get(result)

                return wrapper

            return value


        # Call the getter
        result = get()

        # If the result is a list
        if(isinstance(result, list) and len(result) > 0):
            # Return handled objects
            return [self._handle_get(x) for x in result]

        return self._handle_get(result)


    def __setattr__(self, attr, value):
        # Get the outlet
        outlet = self._views.outlets[self._instance]

        # Get the getter
        setf = getattr(outlet, "set_%s" % attr)

        # If the value is a list
        if(isinstance(value, list) and len(value) > 0):
            # Set handled objects
            return setf([self._handle_set(x) for x in value])

        # Call the setter
        return getf(self._handle_set(value))


    def __iter__(self):
        return iter(self.children)


    def __getitem__(self, key):
        return self.children[key]


    def __setitem__(self, key, value):
        # Get the array
        items = self.children

        # Set the item
        items[key] = value

        # Update the ChildViews
        self._views.set_views(items, self._instance)


    def __delitem__(self, key):
        # Get the array
        items = self.children

        # Delete the item
        del items[key]

        # Update the ChildViews
        self._views.set_views(items, self._instance)


    def add(self, view):
        # Get the array
        items = self.children

        # Add the item
        items.append(view)

        # Update the ChildViews
        self._views.set_views(items, self._instance)


    def reset(self):
        self._views.set_views([], self._instance)

    
    def remove(self, view):
        # Get the array
        items = self.children

        # Find the item
        items.remove(view)

        # Update the ChildViews
        self._views.set_views(items, self._instance)

    