from concurrent.futures import thread
import threading
import queue
import random
import time
import datetime

class Person(threading.Thread):
    def __init__(self, id, queueList, semList, movies):
        threading.Thread.__init__(self)
        self.id = id
        self.room = random.randint(1, 4)
        self.patio_queue = queueList[0]
        self.room_queue = queueList[self.room]
        self.exit_queue = queueList[9]
        self.time = None

        self.line_sem = semList[self.room - 1]
        self.room_sem = semList[self.room + 3]

        self.movie = movies[self.room - 1]

    def run(self):
        patio_central(self)
        fila()
        sala()
        salida()

class Movie():
    def __init__(self, duration, capacity):
        self.duration = duration
        b = threading.Barrier(capacity)
        keep_time = True
        cv = threading.Condition()

def patio_central(person):
    person.time = datetime.datetime.now()

def fila(person):
    person.line_sem.acquire()
    line = "Persona {}, {}, Sala {}, {}"
    cur_time = datetime.datetime.now()
    person.patio_queue.put(line.format(person.id, person.time, person.room, cur_time))
    person.time = cur_time

def sala(person):
    person.room_sem.acquire()
    person.line_sem.release()
    line = "Persona {}, {}, {}"
    cur_time = datetime.datetime.now()
    person.room_queue.put(line.format(person.id, person.time, cur_time))
    person.movie.b.wait()  # Esperar a que se llene la sala

def salida(person):
    while(datetime.datetime.now() - person.time < person.movie.duration):
        pass
    person.room_sem.release()
    line = "Persona {}, {}"
    person.exit_queue.put(line.format(person.id, datetime.datetime.now()))



# Write queues #
# queueList[0] -> patio
# queueList[1 - 4] -> salas
# queueList[5] -> salida
queueList = [ queue.Queue() for i in range(6) ]

# Semaphores #
# semList[0 - 3] -> filas
# semList[4 - 7] -> salas
semList = []
semList.append(threading.Semaphore(10))
semList.append(threading.Semaphore(8))
semList.append(threading.Semaphore(15))
semList.append(threading.Semaphore(10))

semList.append(threading.Semaphore(15))
semList.append(threading.Semaphore(12))
semList.append(threading.Semaphore(25))
semList.append(threading.Semaphore(20))

# Movies #
movies = []
movies.append(Movie(5, 15))
movies.append(Movie(7, 12))
movies.append(Movie(6, 25))
movies.append(Movie(8, 20))


