from LibApplication.Stock.Services.Data.Capsule import Capsule
import uuid

class DataModel(object):

    def __init__(self):
        self.__modified = False

    def _set_state(self, dictionary):
        # Set up our data
        self.__dict__ = dictionary

