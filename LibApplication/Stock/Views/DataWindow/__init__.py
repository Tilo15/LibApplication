from LibApplication.View.Window import WindowView
from LibApplication.View.Binding import Binding, FormattedBinding, IconBinding
from LibApplication.View.ChildView import ChildView
from LibApplication.View.ChildViews import ChildViews

from LibApplication.Stock.Views.DataWindow.DataObject import DataObject

@WindowView("DataWindow.glade", "window")
class DataWindow:

    panes = ChildViews("panes")

    def __init__(self):
        self.panes = []

    def set_root(self, obj, name = "root"):
        self.add_pane(DataObject(obj, name))

    def add_pane(self, data_object):
        # Subscribe to events
        data_object.close.subscribe(lambda x: self.close_pane(data_object))
        data_object.open_right.subscribe(lambda x: self.open_right(data_object, x))
        # Add to the panes
        self.panes.add(data_object)


    def close_pane(self, pane):
        # Get index of pane
        index = self.panes.index(pane)

        # Close window if closing root object
        if(index == 0):
            self.complete()

        # Close all panes to the right
        self.panes = self.panes[:index]

    def open_right(self, pane, member):
        # Is this not the rightmost pane?
        if(len(self.panes) - 1 > self.panes.index(pane)):
            # Close the pane after this one
            self.close_pane(self.panes[self.panes.index(pane) + 1])

        # Add the pane
        self.add_pane(DataObject(member.obj, member.name))

