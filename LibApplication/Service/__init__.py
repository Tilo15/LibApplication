
class ServiceSpawner(object):

    def __init__(self, clas):
        self.clas = clas
        self.instance = None
        self.instanciated = False

    def __get__(self, instance, owner):
        if(not self.instanciated):
            self.instance = self.clas()
            self.instanciated = True

        return self.instance


def Service(clas):
    return ServiceSpawner(clas)
