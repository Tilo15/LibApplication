
class NavigationalDataProxy:

    def __init__(self, obj_id, data_service):
        base = super()
        
        base.__setattr__("object", None)
        base.__setattr__("object_id", obj_id)
        base.__setattr__("data_service", data_service)
        base.__setattr__("has_object", False)

    def get_object(self):
        base = super()

        has_object = base.__getattribute__("has_object")
        if(has_object):
            return base.__getattribute__("object")

        else:
            data_service = base.__getattribute__("data_service")
            object_id = base.__getattribute__("object_id")
            obj = data_service.read_object(object_id)
            base.__setattr__("object", obj)
            base.__setattr__("has_object", True)

            return obj

    def __getattribute__(self, attr):
        obj = NavigationalDataProxy.get_object(self)
        return obj.__getattribute__(attr)

    def __setattr__(self, attr, value):
        obj = NavigationalDataProxy.get_object(self)
        obj.__setattr__(attr, value)