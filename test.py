
from LibApplication.View import View
from LibApplication.View.Binding import Binding

from gi.repository import Gtk

@View("test.glade", "window1")
class MyWindow:

    title = Binding("title", "text")
    subtitle = Binding("subtitle", "text")

    def __init__(self):
        self.count = 0

    def hello_world(self, sender):
        if(self.count == 0):
            self.title = "Hello world!"
            self.subtitle = "For the first time!"
            self.count = 1

        else:
            self.title = "Hello world #%i" % self.count
            self.subtitle = "You have clicked the Hello World button %i times!" % self.count

        self.count += 1


win = MyWindow()
win._root.show_all();

Gtk.main()