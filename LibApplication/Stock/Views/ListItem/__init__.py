from LibApplication.View import View
from LibApplication.View.Event import Event
from LibApplication.View.Binding import Binding


@View("ListItem.glade", "root")
class ListItem:

    title = Binding("title", "text")
    @Binding("subtitle", "text")
    def subtitle(self, subtitle):
        if(subtitle != None):
            self.show_subtitle = True
            return subtitle

        self.show_subtitle = False
        return ""
        
    @Binding("icon", "icon", size = 32)
    def icon(self, icon):
        if(icon != None):
            self.show_icon = True
            return icon
        
        self.show_icon = False
        return "go-next-symbolic"

    show_subtitle = Binding("subtitle", "visible")
    show_icon = Binding("icon", "visible")
    show_button = Binding("button", "visible")

    def __init__(self, title, subtitle = None, icon = None, button = False):
        self.title = title
        self.subtitle = subtitle
        self.icon = icon        
        self.show_button = button