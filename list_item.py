
from LibApplication.View import View
from LibApplication.View.Binding import Binding

from gi.repository import Gtk

@View("list_item.glade", "item")
class ChildView:

    title = Binding("title", "text")
    subtitle = Binding("subtitle", "text")

    def __init__(self, title, subtitle):
        self.title = title
        self.subtitle = subtitle
