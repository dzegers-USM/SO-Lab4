import threading
import queue
import random

class Person(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.room = random.randint(0, 3)

queueList = [ queue.Queue() for i in range(4) ]
    
