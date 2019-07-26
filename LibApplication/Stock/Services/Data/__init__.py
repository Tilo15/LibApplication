from LibApplication.Service import Service
from LibApplication.Loop.Queue import QueueLoop
from LibApplication.Loop.AsTask import AsTask

from LibApplication.Stock.Services.Application import ApplicationService
from LibApplication.Stock.Services.Data.DataModel import DataModel
from LibApplication.Stock.Services.Data.NavigationalDataProxy import NavigationalDataProxy
from LibApplication.Stock.Services.Data.Capsule import Capsule
import queue
import uuid
import dbm.gnu
import ast

PRIMITIVES = [int, float, str, bytes]
STRUCTURES = [list, dict, DataModel]

@Service
class DataService:

    operations_loop = QueueLoop()
    application_service = ApplicationService

    def __init__(self):
        # Create map of data types
        self.data_types = {"NoneType": lambda: None}
        for data_type in PRIMITIVES + STRUCTURES:
            self.data_types[data_type.__name__] = data_type

        self.operations_loop.begin_new_thread()
        self.namespace = self.application_service.namespace
        self.__db = dbm.gnu.open("todo_move_me_{0}".format(self.namespace), 'cf')

    def register_model(self, model):
        self.data_types[model.__name__] = model

    def encapsulate(self, start_obj):
        root_id = uuid.uuid4()

        encapsulation_queue = queue.Queue()
        touched = {id(start_obj): root_id}
        capsules = {}

        encapsulation_queue.put(start_obj)

        while(encapsulation_queue.qsize() != 0):
            # Get the object 
            obj = encapsulation_queue.get()

            # Get the object's identity
            identity: uuid.UUID = touched[id(obj)]

            # Get the type name of the object
            type_name = type(obj).__name__

            # Hold the keys
            keys = []

            # Handle cases
            if(isinstance(obj, DataModel)):
                obj = obj.__dict__

            # Dict
            if(type(obj) == dict):
                keys = obj.keys()

            # List
            elif(type(obj) == list):
                keys = range(len(obj))

            else:
                raise TypeError("Cannot process object of type {0}, objects must be an instance of a DataModel, dict, or list".format(type(obj).__name__))

            # Get ready to hold the new object
            output = type(obj)(obj)

            # Loop over each item in this structure
            for key in keys:
                # Get the object
                child = obj[key]

                # Is it a primitive?
                if(any([isinstance(child, x) for x in PRIMITIVES])):
                    # Yes, encapsulate
                    output[key] = Capsule(child, type(child).__name__)

                elif(any([isinstance(child, x) for x in STRUCTURES])):

                    # This is a structure, has it been touched already?
                    if(id(child) not in touched):
                        # Create an ID for the child
                        child_id = uuid.uuid4()

                        # Touch the child
                        touched[id(child)] = child_id

                        # Add to queue
                        encapsulation_queue.put(child)

                    # Get the child's id
                    child_id: uuid.UUID = touched[id(child)]

                    # Save reference
                    output[key] = Capsule(child_id.bytes, "struct")

                else:
                    raise TypeError("Cannot encapsulate type {0}".format(type(child).__name__))

            # Create and save capsule from output object
            capsules[identity.bytes] = Capsule(output, type_name)

        # Return the capsules, and the root object id
        return capsules, root_id


    def save(self, capsules, root_id):
        for key in capsules:
            self.__db[key] = repr(capsules[key])

        self.__db[b'rootref'] = root_id.bytes

        self.__db.sync()

    
    def decapsulate(self, capsule: Capsule):
        if(capsule.type == "struct"):
            # This object is a reference to another object
            return NavigationalDataProxy(capsule.value, self)

        if(capsule.type in self.data_types):
            # Get it
            obj_type = self.data_types[capsule.type]

            # Is it a primitive?
            if(obj_type in PRIMITIVES):
                # Return the object
                return capsule.value

            elif(obj_type == list):
                # The object is a list
                return [self.decapsulate(Capsule.from_dict(x)) for x in capsule.value]

            elif(obj_type == dict):
                # The object is a dictionary
                output = {}

                # Loop over the dictionary
                for key in capsule.value:
                    # Decapsulate the object
                    output[key] = self.decapsulate(Capsule.from_dict(capsule.value[key]))

                return output

            else:
                # The object is a DataModel
                dictionary = {}

                # Loop over the dictionary representation of the model
                for key in capsule.value:
                    # Decapsulate the object
                    dictionary[key] = self.decapsulate(Capsule.from_dict(capsule.value[key]))

                # Create instance of the model
                model = obj_type()

                # Allow the model to set up its values
                model._set_state(dictionary)

                # Return the model
                return model

        else:
            raise TypeError("Unknown type {0} encountered in stored data".format(capsule.type))
    
    def read_object(self, key):
        # Get it from the db
        data = self.__db[key]

        # Get the capsule
        capsule = Capsule.from_string(data.decode("UTF-8"))

        # Get the object
        return self.decapsulate(capsule)


    def test(self):
        c, r = self.encapsulate(B())
        self.save(c, r)

        o = self.read_object(r.bytes)
        print(o.prim)
        print(o.obj.age)
        print(len(o.dictionary))


# Decorator for registering models
def Persistable(model):
    service = DataService.get_instance()
    service.register_model(model)
    return model

@Persistable
class A(DataModel):
    def __init__(self):
        self.age = 19
        self.name = "Billy" 

@Persistable
class B(DataModel):
    def __init__(self):
        self.prim = 1
        self.obj = A()
        self.friends = [A(), A(), A()]
        self.dictionary = {
            "Hello": "world",
            "Best Friend": self.obj
        }