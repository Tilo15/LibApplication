from LibApplication.View import View
from LibApplication.View.Binding import Binding
from LibApplication.Stock.Services.Application import ApplicationService

import rx

def WindowView(path, root_id):

    # Create the decorator function
    def decorator(obj):
        # Get base view function
        view = View(path, root_id)

        # Get base view class
        view_component = view(obj)

        # Extend the base class
        class TopLevelViewComponent(view_component):
            
            _modal = Binding(root_id, 'modal')

            deletable = Binding(root_id, 'deletable')
            resizable = Binding(root_id, 'resizable')
            title = Binding(root_id, 'title')
            urgent = Binding(root_id, 'urgency_hint')

            def __init__(self, *args, **kwargs):
                # Call the base class's init
                view_component.__init__(self, *args, **kwargs)

                # Register the window with the application service
                ApplicationService.get_instance().add_window(self)
                

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
                    self._modal = False
                    self._root.set_transient_for(None)
                    self._root.show()
                else:
                    self._root.hide()

            def hide(self):
                self.show(False)

            def complete(self):
                self._root.close()
                self._root.destroy()

            def show_modal(self, attachment):
                # TODO Tidy Up
                self._modal = True
                # Does it have a parent window?
                parent = attachment._root.get_parent_window()
                if(parent != None):
                    self._root.set_transient_for(parent)
                else:
                    self._root.set_transient_for(attachment._root)

                self._root.show()

            def __del__(self):
                self.complete()

        return TopLevelViewComponent

    return decorator