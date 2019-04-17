from LibApplication.Loop import Loop
import queue
import traceback
import threading

class QueueLoop(Loop):

    def __init__(self):
        # Create the queue that backs the loop
        self.queue = queue.Queue()
        self.alive = False

    def begin(self):
        # Register the loop
        self.register()
        
        # We are alive!
        self.alive = True

        # Start doin it
        while self.alive:
            # Read from queue
            task = self.queue.get()

            # Try and run the task
            try:
                task[0](*task[1])
            except Exception as e:
                print("\nException occurred inside QueueLoop:")
                traceback.print_exc()


    def stop(self):
        # Set to not alive
        self.alive = False

        # Run function to execute loop one more time
        self.run(lambda: False)


    def run(self, call, *args):        
        # Put the call and the arguments into the queue
        self.queue.put((call, args))


    def begin_new_thread(self):
        threading.Thread(target=self.begin).start()
