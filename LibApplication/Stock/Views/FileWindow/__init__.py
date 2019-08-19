from LibApplication.View.Window import WindowView
from LibApplication.View.Binding import Binding, FormattedBinding, IconBinding
from LibApplication.View.ChildView import ChildView
from LibApplication.View.Event import Event
from LibApplication.Stock.Views.MessageBox import MessageBox

from gi.repository import Gtk
import os

FILE_DIALOG_SAVE = 0
FILE_DIALOG_OPEN = 1
FILE_DIALOG_FOLDER = 2
FILE_DIALOG_OPEN_MANY = 3

@WindowView("FileWindow.glade", "root")
class FileWindow:
    options = ChildView("child")
    file = Binding("root", "filename")
    files = Binding("root", "filenames")
    multiple = Binding("root", "select_multiple")
    action = Binding("root", "action")

    def __init__(self, window_type = FILE_DIALOG_SAVE, filters = {}):
        self.extension = ""
        self.window_type = window_type

        bar = self._root.get_header_bar()
        bar.pack_start(self._builder.get_object("cancel"))

        if(window_type == FILE_DIALOG_SAVE):
            bar.pack_end(self._builder.get_object("save"))
            self.action = Gtk.FileChooserAction.SAVE
            self.title = "Save As"

        else:
            bar.pack_end(self._builder.get_object("open"))

            if(window_type == FILE_DIALOG_OPEN or window_type == FILE_DIALOG_OPEN_MANY):
                self.title = "Please Select a File…"
                self.action = Gtk.FileChooserAction.OPEN

            elif(window_type == FILE_DIALOG_FOLDER):
                self.title = "Please Select a Folder…"
                self.action = Gtk.FileChooserAction.SELECT_FOLDER

        # Allow multiple select if open many
        self.multiple = window_type == FILE_DIALOG_OPEN_MANY

        # Construct filters
        for name, types in filters.items():
            gtk_filter = Gtk.FileFilter()
            gtk_filter.set_name(name)
            filter_items = types
            # If it is a single string, convert to array with one item
            if(isinstance(types, str)):
                filter_items = [types,]

            for item in filter_items:
                if("*" in item):
                    gtk_filter.add_pattern(item)
                else:
                    gtk_filter.add_mime_type(item)
                    
            self._root.add_filter(gtk_filter)

    
    @Event
    def cancel(self):
        self.hide()

    @Event
    def _select(self):
        if(self.window_type == FILE_DIALOG_SAVE):
            if(not self.file.endswith(self.extension)):
                self.file += self.extension

            if(os.path.exists(self.file)):
                msg = MessageBox("A file named “%s” already exists" % self.file.split("/")[-1], "The filename you have chosen conflicts with an already existing file. Continuing will overwrite its contents.", ["Cancel", "Overwrite"])
                msg.dismissed.subscribe(self._confirm)
                msg.show_modal(self)

            else:
                self.select()
        
        else:
            self.select()

                
    def _confirm(self, result):
        if(result == 1):
            self.select()

    @Event
    def select(self):
        self.hide()

        if(self.window_type == FILE_DIALOG_OPEN_MANY):
            return self.files

        return self.file