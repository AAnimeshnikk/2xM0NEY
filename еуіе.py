from threading import Thread
from DB_account import *

def x():
    a = 1
    while True:
        print(2)
        CreateNewAccount(a, "")
        a += 1

def y():
    a = 0
    while True:
        print(1)
        CreateNewAccount(a, "")
        a -= 1

th1 = Thread(target=x)
th2 = Thread(target=y)
th1.start()
th2.start()