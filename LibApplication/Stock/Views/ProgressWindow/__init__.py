from LibApplication.View.Window import WindowView
from LibApplication.View.Binding import Binding, FormattedBinding, IconBinding
from LibApplication.View.ChildView import ChildView

@WindowView("ProgressWindow.glade", "window")
class ProgressWindow:
    heading = Binding("heading", "text")
    subheading = Binding("subheading", "text")
    icon = IconBinding("icon", 48)
    prompt = ChildView("prompt")
    progress = Binding("progress", "fraction")

    @FormattedBinding("stack", "visible_child_name")
    def show_prompt(self, visible):
        if(visible):
            return "view"
        else:
            return "progress"