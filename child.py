
from LibApplication.View import View
from LibApplication.View.Binding import Binding

from gi.repository import Gtk

@View("child.glade", "meme")
class ChildView:

    def __init__(self):
        pass
