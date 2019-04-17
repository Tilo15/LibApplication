from gi.repository import Gtk
from gi.repository import Gdk

def load_css(path):
    cssProvider = Gtk.CssProvider()
    cssProvider.load_from_path(path)
    screen = Gdk.Screen.get_default()
    styleContext = Gtk.StyleContext()
    styleContext.add_provider_for_screen(screen, cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER) 