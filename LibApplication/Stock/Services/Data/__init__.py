from LibApplication.Service import Service
from LibApplication.Loop.Queue import QueueLoop
from LibApplication.Loop.AsTask import AsTask

from LibApplication.Stock.Services.Application import ApplicationService
from LibApplication.Stock.Services.Data.DataModel import DataModel
from LibApplication.Stock.Services.Data.Capsule import Capsule

from lazy_object_proxy import Proxy

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
        self.___db = None
        self.loaded_items = {}
        self.db_refs = {}

    @property
    def __db(self):
        if(self.___db == None):
            self.___db = dbm.gnu.open("todo_move_me_{0}".format(self.application_service.namespace), 'cf')

        return self.___db

    def register_model(self, model):
        self.data_types[model.__name__] = model

    def encapsulate(self, start_obj):
        # Generate an id for our first object
        first_id = uuid.uuid4()

        # Was this object loaded from the DB?
        if(id(start_obj) in self.db_refs):
            # Use that ID instead
            first_id = self.db_refs[id(start_obj)]

        encapsulation_queue = queue.Queue()
        touched = {id(start_obj): first_id}
        capsules = {}

        encapsulation_queue.put(start_obj)

        while(encapsulation_queue.qsize() != 0):
            # Get the object 
            obj = encapsulation_queue.get()

            # Get the object's identity
            identity: uuid.UUID = touched[id(obj)]

            # Save it to our identity tracker
            self.db_refs[id(obj)] = identity.bytes

            # TODO look at also saving this to loaded_items at this point too

            # Get the type name of the object
            type_name = type(obj).__name__

            # Hold the keys
            keys = []

            # Handle cases
            if(isinstance(obj, DataModel)):
                obj = obj.__dict__

            # Dict
            if(isinstance(obj, dict)):
                keys = obj.keys()

            # List
            elif(isinstance(obj, list)):
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

                        # Does this child have an ID already?
                        if(id(child) in self.db_refs):
                            # Use that instead
                            child_id = self.db_refs[id(child)]

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

        # Return the capsules, and the first object's id
        return capsules, first_id


    def save_capsules(self, capsules, root_id = None):
        for key in capsules:
            self.__db[key] = repr(capsules[key])

        if(root_id != None):
            self.__db[b'rootref'] = root_id.bytes

        self.__db.sync()

    
    def decapsulate(self, capsule: Capsule):
        if(capsule.type == "struct"):
            # This object is a reference to another object
            return Proxy(lambda: self.read_object(capsule.value))

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
                    child = self.decapsulate(Capsule.from_dict(capsule.value[key]))
                    dictionary[key] = child

                # Create instance of the model
                model = obj_type()

                # Allow the model to set up its values
                model._set_state(dictionary)


                # Return the model
                return model

        else:
            raise TypeError("Unknown type {0} encountered in stored data".format(capsule.type))
    
    def read_object(self, key):
        print("call")
        # Do we have it already?
        if(key in self.loaded_items):
            return self.loaded_items[key]

        print("db hit")

        # Get it from the db
        data = self.__db[key]

        # Get the capsule
        capsule = Capsule.from_string(data.decode("UTF-8"))

        # Get the object
        obj = self.decapsulate(capsule)

        # Cache the object
        self.loaded_items[key] = obj
        
        # Save db ref
        self.db_refs[id(obj)] = key

        # Return to caller
        return obj

    def get_root_id(self):
        return self.__db[b"rootref"]

    def test(self):
        b = B()
        b.obj.name = "John-William"
        c, r = self.encapsulate(b)
        self.save_capsules(c, r)

        o = self.read_object(r.bytes)
        print(o.prim)
        print(o.friends)
        print(o.obj)
        print(o.dictionary)
        print(o.dictionary)
        print(o.dictionary["Best Friend"])


    @AsTask(operations_loop)
    def get(self):
        # Get the root object's ID
        root_id = self.get_root_id()

        # Return the root object
        return self.read_object(root_id)


    @AsTask(operations_loop)
    def set_root(self, obj):
        # Encapsulate the object
        capsules, obj_id = self.encapsulate(obj)

        # Save the capsules, updating the root id
        self.save_capsules(capsules, obj_id)

    @AsTask(operations_loop)
    def save(self, obj):
        # Is this object connected to anything in our graph?
        if(id(obj) not in self.db_refs):
            raise ValueError("Cannot save an object to the database that is not directly or indirectly connected to the root object")

        # Encapsulate the object
        capsules, obj_id = self.encapsulate(obj)

        # Save the capsules, keeping the current root id
        self.save_capsules(capsules)

    


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

    def __str__(self):
        return "{0} ({1})".format(self.name, self.age)

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