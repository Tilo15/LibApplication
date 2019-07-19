
from LibApplication.View.Window import WindowView
from LibApplication.View.Binding import Binding, FormattedBinding
from LibApplication.View.ChildView import ChildView
from LibApplication.View.ChildViews import ChildViews

from LibApplication.Stock.Views.ProgressWindow import ProgressWindow
from LibApplication.Stock.Services.Http import HttpService
from LibApplication.Stock.Services.PinEntry import PinEntryService

from gi.repository import Gtk

import child, bean, list_item

@WindowView("test.glade", "window1")
class MyWindow:

    title = Binding("title", "text")
    show_list = Binding("list_reveal", "reveal_child")
    viewport = ChildView("viewport")
    list_view = ChildViews("list")

    http = HttpService
    pin_entry = PinEntryService

    def __init__(self):
        self.count = 0
        self.progress = ProgressWindow()

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

            self.pin_entry.get_pin("Unlock identity 'Billy Barrow'", "In order to continue, you must unlock identity information for your 'Billy Barrow' profile.").subscribe(lambda x: print(x))

            array = [
                ("Item 1", "This is a cool item"),
                ("Item 2", "This is a cooler item"),
                ("Item 3", "This is a pre-defined array"),
                ("Here, I'll prove it", "See?")
            ]

            self.list_view = list_item.ChildView.bulk(array)
            self.show_list = True

            print(self.list_view)

        self.count += 1

        if(self.count == 6):
            del self.list_view[2]

        if(self.count == 8):
            self.list_view.add(list_item.ChildView("I was added later", "I'm special"))
            self.list_view.select_row(self.list_view[3])

        if(self.count == 12):
            self.list_view.unselect_all()

        if(self.count == 31):
            self.show_list = False
            self.progress.icon = "computer"

        if(self.count == 32):
            self.list_view.reset()

        if(self.count == 3):
            self.progress.show()
            self.progress.icon = "software-update-available"
            self.progress.heading = "Yeet"
            self.progress.subheading = "Skadeet"
            self.progress.show_prompt = False

        if(self.count > 3):
            self.progress.progress = self.count / 40.0
            self.progress.title = "Operating System Installer"

        if(self.count == 40):
            self.progress.prompt = bean.ChildView()
            self.progress.show_prompt = True
            self.progress.maximize()

        if(self.count == 50):
            self.count = 0
            self.progress.maximize(False)



    @FormattedBinding("subtitle", "text")
    def subtitle(self, value):
        return "You've clicked the Hello World button %i times!" % self.count


    def get_something(self, sender):
        self.http.get("http://api.geonet.org.nz/intensity?type=measured").subscribe(self.print_response)

    def print_response(self, response):
        print(response)
