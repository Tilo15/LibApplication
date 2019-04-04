
class ChildViews(object):
    
    def __init__(self, ui_id, view_type):
        self.ui_id = ui_id
        self.view_type = view_type
        self.views = {}


    def __set__(self, instance, values):
        # Get builder
        builder = getattr(instance, "_builder", None)

        # Error if no builder
        if(builder == None):
            raise TypeError("Outlets can only exist on classes with a '@View' decorator.")

        # Get the outlet
        outlet = builder.get_object(self.ui_id)

        # Build the views
        view_type = self.view_type
        views = []

        for value in values:
            views.append(view_type(*value))

        # Remove children
        children = outlet.get_children()
        for child in children:
            outlet.remove(child)

        # Add views
        for view in views:
            outlet.add(view._root)
            view._root.show_all()

        # Save views
        self.views[instance] = views


    def __get__(self, instance, owner):
        if(instance in self.views):
            return ChildViewsIterator(self.views[instance])

        return None


class ChildViewsIterator(object):

    def __init__(self, views):
        super().__setattr__("views", views)


    def __getattribute__(self, attr):
        views = super().__getattribute__("views")

        results = []
        for view in views:
            results.append(getattr(view, attr))

        return results

    def __setattr__(self, attr, value):
        views = super().__getattribute__("views")

        for view in views:
            setattr(view, attr, value)

    def __iter__(self):
        views = super().__getattribute__("views")
        return iter(views)



    