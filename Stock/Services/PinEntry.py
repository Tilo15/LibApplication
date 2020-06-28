from LibApplication.Service import Service
from LibApplication.Loop.Queue import QueueLoop
from LibApplication.Loop.AsTask import AsTask

import subprocess

@Service
class PinEntryService:

    requestLoop = QueueLoop()

    def __init__(self):
        self.requestLoop.begin_new_thread()

    def _run(self, process, command):
        process.stdin.write("{0}\n".format(command))
        process.stdin.flush()
        out = process.stdout.readline()

        if(out == "OK\n"):
            return True
        return False


    @AsTask(requestLoop)
    def confirm(self, message, description, okay_button = "Continue", cancel_button = "Cancel"):
        process = subprocess.Popen(["/bin/pinentry-gtk",], stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True);
        process.stdout.readline()
        
        self._run(process, "SETPROMPT {0}".format(message))
        self._run(process, "SETDESC {0}".format(description))
        self._run(process, "SETOK {0}".format(okay_button))
        self._run(process, "SETCANCEL {0}".format(cancel_button))

        return self._run(process, "CONFIRM")

    
    @AsTask(requestLoop)
    def get_pin(self, message, description, error="", okay_button = "Continue", cancel_button = "Cancel"):
        process = subprocess.Popen(["/bin/pinentry",], stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True);
        process.stdout.readline()
        
        self._run(process, "SETPROMPT {0}".format(message))
        self._run(process, "SETDESC {0}".format(description))
        self._run(process, "SETOK {0}".format(okay_button))
        self._run(process, "SETCANCEL {0}".format(cancel_button))
        self._run(process, "SETERROR {0}".format(error))

        process.stdin.write("GETPIN\n")
        process.stdin.flush()

        out = process.stdout.readline()
        if(out[0] == "D" or out == "OK\n"):
            return out[2:-1]

        return None
