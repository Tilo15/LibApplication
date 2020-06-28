import LibApplication.Stock.Services.Data as Data
import ast

class Capsule:
    
    def __init__(self, value, typeid):
        self.value = value
        self.type = typeid

    def __repr__(self):
        return self.__dict__.__repr__()

    @staticmethod
    def from_string(string):
        # Evaliate dictionary
        obj = ast.literal_eval(string)
        return Capsule.from_dict(obj)

    @staticmethod
    def from_dict(obj):
        # Create new capsule
        return Capsule(obj["value"], obj["type"])