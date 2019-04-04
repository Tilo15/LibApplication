from LibApplication.Util.Static import WithReferenceOwner

@WithReferenceOwner
class Outlet(object):

    def __init__(self, ui_id):
        self.ui_id = ui_id


    def get_component(self, instance):
        # Get builder
        builder = getattr(instance, "_builder", None)

        # Error if no builder
        if(builder == None):
            raise TypeError("Outlets can only exist on classes with a '@View' decorator.")

        return builder.get_object(self.ui_id)


    def display(self, instance, view):
        # Get the GTK component
        outlet = self.get_component()

        # Reset view
        self.reset()

        # Add view
        outlet.add(view._root)

        # Show
        view._root.show_all()

    def reset(self, instance):
        # Get the GTK component
        outlet = self.get_component()

        # Remove children
        children = outlet.get_children()
        for child in children:
            outlet.remove(child)

