from LibApplication.View import View
from LibApplication.View.Binding import Binding
from LibApplication.View.ChildView import ChildView
from LibApplication.View.ChildViews import ChildViews
from LibApplication.View.Event import Event

from LibApplication.Stock.Views.DataWindow.DataMember import DataMember

@View("DataObject.glade", "root")
class DataObject:
    name = Binding("title", "text")
    items = ChildViews("members")

    open_right = Event()

    close = Event()

    def __init__(self, obj, name):
        self.name = name

        # If the object is a list
        if(isinstance(obj, list)):
            # Create based on index
            self.items = DataMember.bulk(((obj[x], str(x)) for x in range(len(obj))))

        elif(isinstance(obj, dict)):
            # Create based on keys
            self.items = DataMember.bulk(((obj[x], repr(x)) for x in obj.keys()))

        else:
            # Create based on object values
            obj_dict = obj.__dict__
            self.items = DataMember.bulk(((obj_dict[x], x) for x in obj_dict.keys()))

    @Event
    def navigate(self):
        # Get the selected item
        item = self.items.selected_row

        # Is the item navigatable?
        if(item.navigatable):
            self.open_right(item)

            



        