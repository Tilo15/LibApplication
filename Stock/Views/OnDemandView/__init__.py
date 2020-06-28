from LibApplication.View import View
from LibApplication.View.Binding import Binding
from LibApplication.View.ChildView import ChildView
from LibApplication.View.Event import Event

from gi.repository import GLib

@View("OnDemandView.glade", "root")
class OnDemandView:
    child = ChildView("reveal")
    loaded = Binding("reveal", "reveal_child")
    
    def __init__(self, constructor, observable):
        self._constructor = constructor
        self._observable = observable
        self.loading = False

    @Event
    def draw(self):
        if(not self.loading and not self.loaded):
            self.loading = True
            def init(params):
                instance = self._constructor(params)
                print(self, "draw", params, self._constructor, instance)
                self.child = instance
                self.loaded = True
                self.loading = False
                self.child._root.show()
            
            self.child = self._observable.subscribe(init)
