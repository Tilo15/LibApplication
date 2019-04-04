
class ChildView(object):

    def __init__(self, ui_id):
        self.ui_id = ui_id
        self.views = {}


    def get_component(self, instance):
        # Get builder
        builder = getattr(instance, "_builder", None)

        # Error if no builder
        if(builder == None):
            raise TypeError("Outlets can only exist on classes with a '@View' decorator.")

        return builder.get_object(self.ui_id)


    def __set__(self, instance, view):
        # Get the GTK component
        outlet = self.get_component(instance)

        # Reset view
        self.reset(outlet)

        # Add view
        outlet.add(view._root)

        # Show
        view._root.show_all()

        # Keep reference to view
        self.views[instance] = view


    def reset(self, outlet):
        # Remove children
        children = outlet.get_children()
        for child in children:
            outlet.remove(child)

    
    def __get__(self, instance, owner):
        if(instance in self.views):
            return self.views[instance]
        else:
            return None

    

