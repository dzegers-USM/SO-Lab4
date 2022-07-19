import threading
import queue
import random
import time, datetime
import sys, os, errno

TIMEOUT = 10  # Segundos

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
        self.exit_queue = queueList[5]          # Salida.txt

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

def patio_central(person):
    # No hay limitaciones al flujo de gente por el patio central, luego
    # solo necesitamos registrar el tiempo de llegada
    person.time = datetime.datetime.now()

def fila(person):
    person.line_sem.acquire()
    printOut = "Persona {}, {}, Sala {}, {}\n"
    cur_time = datetime.datetime.now()
    person.patio_queue.put(printOut.format(person.id, person.time.time(),
                                           person.room, cur_time.time()))
    person.time = cur_time

def sala(person):
    person.room_sem.acquire()
    person.line_sem.release()
    printOut = "Persona {}, {}, {}\n"
    cur_time = datetime.datetime.now()
    person.room_queue.put(printOut.format(person.id, person.time.time(),
                                          cur_time.time()))
    try:
        person.movie.barrier.wait(timeout=TIMEOUT)
    except threading.BrokenBarrierError:
        pass
    person.time = datetime.datetime.now()

def salida(person):
    time_diff = datetime.datetime.now() - person.time
    while(time_diff.seconds < person.movie.duration):
        time_diff = datetime.datetime.now() - person.time
        time.sleep(1)
    person.room_sem.release()
    printOut = "Persona {}, {}\n"
    cur_time = datetime.datetime.now()
    person.exit_queue.put(printOut.format(person.id, cur_time.time()))

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

# Main thread #
people = []
for i in range(100):
    people.append(Person(i + 1, queueList, semList, movies))

for person in people:
    person.start()

for person in people:
    person.join()

try:
    os.mkdir("out")
except OSError as e:
    if e.errno != errno.EEXIST:
        print(e)
        sys.exit(e.errno)

fnames = ["PatioCentral.txt", "Sala1.txt", "Sala2.txt",
          "Sala3.txt", "Sala4.txt", "Salida.txt"]
for i, q in enumerate(queueList):
    with open("out/" + fnames[i], 'w') as f:
        while q.qsize() != 0:
            f.write(q.get())
sys.exit(0)
