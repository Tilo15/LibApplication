
from LibApplication.View import View
from LibApplication.View.Binding import Binding, FormattedBinding
from LibApplication.View.ChildView import ChildView
from LibApplication.View.ChildViews import ChildViews

from gi.repository import Gtk

import child, bean, list_item

@View("test.glade", "window1")
class MyWindow:

    title = Binding("title", "text")
    show_list = Binding("list_reveal", "reveal_child")
    viewport = ChildView("viewport")
    list_view = ChildViews("list", list_item.ChildView)

    def __init__(self):
        self.count = 0

    def hello_world(self, sender):
        if(self.count == 0):
            self.title = "Hello world for the first time!"
            self.count = 1

        else:
            self.title = "Hello world #%i" % self.count

        self.subtitle = self.count

        if(self.count == 10):
            self.viewport = child.ChildView()

        if(self.count == 20):
            self.viewport = bean.ChildView()

        if(self.count == 2):
            array = [
                ("Item 1", "This is a cool item"),
                ("Item 2", "This is a cooler item"),
                ("Item 3", "This is a pre-defined array"),
                ("Here, I'll prove it", "See?")
            ]

            self.list_view = array
            self.show_list = True

            print(self.list_view.title)

        self.count += 1


    @FormattedBinding("subtitle", "text")
    def subtitle(self, value):
        return "You've clicked the Hello World button %i times!" % self.count
    


for i in range(5):
    win = MyWindow()
    win._root.show_all();

Gtk.main()