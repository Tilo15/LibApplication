from LibApplication.View import View
from LibApplication.View.Binding import Binding

def WindowView(path, root_id):

    # Create the decorator function
    def decorator(obj):
        # Get base view function
        view = View(path, root_id)

        # Get base view class
        viewComponent = view(obj)

        # Extend the base class
        class TopLevelViewComponent(viewComponent):
            
            _modal = Binding(root_id, 'modal')

            deletable = Binding(root_id, 'deletable')
            resizable = Binding(root_id, 'resizable')
            title = Binding(root_id, 'title')
            urgent = Binding(root_id, 'urgency_hint')


            def fullscreen(self, state = True):
                if(state):
                    self._root.fullscreen()
                else:
                    self._root.unfullscreen()

            def maximize(self, state = True):
                if(state):
                    self._root.maximize()
                else:
                    self._root.unmaximize()

            def minimize(self, state = True):
                if(state):
                    self._root.iconify()
                else:
                    self._root.deiconify()

            def stick(self, state = True):
                if(state):
                    self._root.stick()
                else:
                    self._root.unstick()

            def topmost(self, state = True):
                self._root.set_keep_above(state)

            def show(self, state = True):
                if(state):
                    self._root.show_all()
                else:
                    self._root.hide()

            def hide(self):
                self.show(False)

            def complete(self):
                self._root.close()

            def __del__(self):
                self.complete()

        return TopLevelViewComponent

    return decorator