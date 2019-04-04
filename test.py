
from LibApplication.View import View
from LibApplication.View.Binding import Binding
from LibApplication.View.Outlet import Outlet

from gi.repository import Gtk

import child, bean

@View("test.glade", "window1")
class MyWindow:

    title = Binding("title", "text")
    subtitle = Binding("subtitle", "text")
    viewport = Outlet("viewport")

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

        if(self.count == 10):
            child_view = child.ChildView()
            self.viewport.display(child_view)

        if(self.count == 20):
            child_view = bean.ChildView()
            self.viewport.display(child_view)

        self.count += 1


win = MyWindow()
win._root.show_all();

Gtk.main()