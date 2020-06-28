from LibApplication.View.Window import WindowView
from LibApplication.View.Binding import Binding
from LibApplication.View.ChildView import ChildView

@WindowView("ProgressWindow.glade", "window")
class ProgressWindow:
    heading = Binding("heading", "text")
    subheading = Binding("subheading", "text")
    icon = Binding("icon", "icon", size = 48)
    progress = Binding("progress", "fraction")
    prompt = ChildView("prompt")

    @Binding("stack", "visible_child_name")
    def show_prompt(self, visible):
        if(visible):
            return "view"
        else:
            return "progress"