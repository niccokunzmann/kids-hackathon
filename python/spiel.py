import os
from threading import local
import sys
import socket

_du = threading.local()

alle_spieler = []

class Spieler(object):
    pass

def du():
    try:
       return _du.spieler
    except:
        _du.spieler = Spieler()
        alle_spieler.append(_du.spieler)
        return _du.spieler

class IO(threading.local):
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    file = None
    def set_socket(self, socket):
        self.socket = socket
        self.file = self.socket.makefile('rb')

    def read(self, size):
        if self.file:
            return self.file.read(size)
        return self.old_stdin.read(size)

    def write(self, string):
        if self.file:
            return self.file.write(string)
        return self.old_stdout.write(size)

sys.stdin = sys.stdout = IO()

def gehe_zu(raum):
    if not os.path.isfile(raum):
        print('den raum gibt es leider nicht.')
        return
    
    
