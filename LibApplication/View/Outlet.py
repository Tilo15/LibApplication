from LibApplication.Util.Static import WithReferenceOwner

@WithReferenceOwner
class Outlet(object):

    def __init__(self, ui_id):
        self.ui_id = ui_id


    def show_view(self, instance, view):
        # Get builder
        builder = getattr(instance, "_builder", None)

        # Error if no builder
        if(builder == None):
            raise TypeError("Outlets can only exist on classes with a '@View' decorator.")

        # Get the GTK component
        outlet = builder.get_object(self.ui_id)

        # Remove any children
        children = outlet.get_children()
        for child in children:
            outler.remove(child)

        # Add view
        outlet.add(view._root)

        # Show
        view._root.show_all()
