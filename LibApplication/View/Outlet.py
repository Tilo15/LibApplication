from LibApplication.Util.Static import WithReferenceOwner

@WithReferenceOwner
class Outlet(object):

    def __init__(self, ui_id):
        self.ui_id = ui_id


    def _get_builder(self, instance):
        # Get builder
        builder = getattr(instance, "_builder", None)

        # Error if no builder
        if(builder == None):
            raise TypeError("Outlets can only exist on classes with a '@View' decorator.")

        return builder


    def display(self, instance, view):
        builder = self._get_builder()

        # Get the GTK component
        outlet = builder.get_object(self.ui_id)

        # Remove any children
        children = outlet.get_children()
        for child in children:
            outlet.remove(child)

        # Add view
        outlet.add(view._root)

        # Show
        view._root.show_all()