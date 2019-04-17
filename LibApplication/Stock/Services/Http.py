from LibApplication.Service import Service
from LibApplication.Loop.Queue import QueueLoop
from LibApplication.Loop.AsTask import AsTask

import requests

# TODO: Way more

@Service
class HttpService:

    requestLoop = QueueLoop()

    def __init__(self):
        self.requestLoop.begin_new_thread()
        self.s = requests.sessions.Session()

    @AsTask(requestLoop)
    def get(self, url):
        return self.s.get(url)