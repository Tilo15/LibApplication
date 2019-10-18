from LibApplication.View import View
from LibApplication.View.Binding import Binding, FormattedBinding, IconBinding
from LibApplication.View.ChildView import ChildView

from LibApplication.Stock.Services import Data

@View("DataMember.glade", "root")
class DataMember:
    name = Binding("name", "text")
    value = Binding("value", "text")
    navigatable = Binding("navigate", "visible")

    def __init__(self, value, name):
        self.name = name
        self.value = ""
        self.obj = value

        # Is the value a primitive?
        if(any([isinstance(value, x) for x in Data.PRIMITIVES])):
            self.value = repr(value)
            self.navigatable = False

        else:
            # Use type name as value
            self.value = value.__class__.__name__
            self.navigatable = True

        
