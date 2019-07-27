from LibApplication.Stock.Services.Data.Capsule import Capsule
import uuid

class DataModel(object):

    def __init__(self):
        self.__modified = False

    def _set_state(self, dictionary, opt = None):
        
        # Set up our data
        # print(self)
        # print(dictionary)
        # print("---")
        if(type(dictionary) == dict):
            self.__dict__ = dictionary
        else:
            print("It was a:")
            print(type(self))

            print(type(dictionary))
            if(type(dictionary) == str):
                print(dictionary)
            print(type(opt))
