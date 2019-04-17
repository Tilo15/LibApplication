from LibApplication.Loop import Loop

from gi.repository import GLib
from gi.repository import Gtk


class GLibLoop(Loop):

    def begin(self):
        self.register()
        Gtk.main()

    def stop(self):
        Gtk.main_quit()

    def run(self, call, *args):
        GLib.idle_add(call, *args)