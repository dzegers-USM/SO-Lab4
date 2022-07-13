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
        self.movie = movies[self.room - 1]
        self.time = None

        # Write Queues #
        self.patio_queue = queueList[0]         # PatioCentral.txt
        self.room_queue = queueList[self.room]  # Sala{room}.txt
        self.exit_queue = queueList[9]          # Salida.txt

        # Semaphores #
        self.line_sem = semList[self.room - 1]
        self.room_sem = semList[self.room + 3]

    def run(self):
        patio_central(self)
        fila(self)
        sala(self)
        salida(self)

class Movie():
    def __init__(self, duration, capacity):
        self.duration = duration
        self.barrier = threading.Barrier(capacity)
        self.lock = threading.Lock()
        self.ready = True

def patio_central(person):
    person.time = datetime.datetime.now()

def fila(person):
    person.line_sem.acquire()
    line = "Persona {}, {}, Sala {}, {}"
    cur_time = datetime.datetime.now()
    person.patio_queue.put(line.format(person.id, person.time, person.room, cur_time))
    person.time = cur_time

def sala(person):
    while not person.movie.ready:
        time.sleep(1)
    person.room_sem.acquire()
    person.line_sem.release()
    line = "Persona {}, {}, {}"
    person.room_queue.put(line.format(person.id, person.time, datetime.datetime.now()))
    person.movie.barrier.wait()  # Esperar a que se llene la sala
    if person.movie.ready:       # Se cierra la entrada hasta que salgan todos de la sala
        person.movie.ready = False
    person.time = datetime.datetime.now()

def salida(person):
    while(datetime.datetime.now() - person.time < person.movie.duration):
        time.sleep(1)
    person.room_sem.release()
    line = "Persona {}, {}"
    person.exit_queue.put(line.format(person.id, datetime.datetime.now()))
    person.movie.barrier.wait()
    if not person.movie.ready:  # Habiendo salido todos, se abre la entrada
        person.movie.ready = True



# Write queues #
# queueList[0] -> patio
# queueList[1 - 4] -> salas
# queueList[5] -> salida
queueList = [ queue.Queue() for i in range(6) ]

# Semaphores #
# semList[0 - 3] -> filas
semList = []
semList.append(threading.Semaphore(10))
semList.append(threading.Semaphore(8))
semList.append(threading.Semaphore(15))
semList.append(threading.Semaphore(10))
# semList[4 - 7] -> salas
semList.append(threading.Semaphore(15))
semList.append(threading.Semaphore(12))
semList.append(threading.Semaphore(25))
semList.append(threading.Semaphore(20))

# Movies #
movies = []
movies.append(Movie(5, 15))  # Minions
movies.append(Movie(7, 12))  # Thor
movies.append(Movie(6, 25))  # Lightyear
movies.append(Movie(8, 20))  # Doctor Strange


