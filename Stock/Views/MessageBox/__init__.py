from LibApplication.View.Window import WindowView
from LibApplication.View.Event import Event

from gi.repository import Gtk


@WindowView("MessageBox.glade", "root")
class MessageBox:

    def __init__(self, heading, subheading, buttons = ["Okay"]):
        print(heading, subheading, buttons)
        self._root.set_markup("<b><big>%s</big></b>" % heading)
        self._root.format_secondary_markup(subheading)
        self._buttons = {}

        button_box = self._builder.get_object("buttons")
        for i, button in enumerate(buttons):
            gtk_button = Gtk.Button(button)
            gtk_button.show()
            button_box.add(gtk_button)
            self._buttons[gtk_button] = i
            gtk_button.connect("clicked", self.dismissed)

    @Event
    def dismissed(self, sender):
        self.hide()
        if(sender in self._buttons):
            return self._buttons[sender]
        else:
            return -1

            