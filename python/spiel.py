#!/usr/bin/python2
import os
from threading import local
import sys
import socket
import traceback
import threading
import time

################ Ein und ausgabe fuer die Verbindungen

class IO(threading.local):
    stdin = sys.stdin
    stdout = sys.stdout
    socket = None
    
    def flush_stdout(self):
        pass
    
    def set_socket(self, socket):
        self.socket = socket
        self.stdin = self.stdout = self.socket.makefile('rb')
        self.flush_stdout = self.stdout.flush

    def read(self, size):
        return self.stdin.read(size)

    def readline(self):
        return self.stdin.readline()

    def write(self, string):
        try:
            self.stdout.write(string)
            self.flush_stdout()
        except socket.error:
            pass


stdio = sys.stdin = sys.stdout = IO()

################ Verbindungen herstellen

BROADCAST_PORT = 13719

s = socket.socket(socket.AF_INET)
s.bind(('0.0.0.0', 0))
s.listen(1)
_, PORT_VERBINDUNG = s.getsockname()

def verbindungen_annehmen(s):
    try:
        while 1:
            sock, addr = s.accept()
            thread = threading.Thread(target = behandle_spieler_verbindung, \
                                      args = (sock,))
            thread.start()
    except:
        traceback.print_exc()
    print('Jetzt kann man sich nicht mehr hierher verbinden.')
    s.close()

thread = threading.Thread(target = verbindungen_annehmen, args = (s,))
thread.start()

def broadcast():
    # momentan nur ipv4
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    try:
        while 1:
            s.sendto(socket.gethostname() + ":" + str(PORT_VERBINDUNG), 
                     ('255.255.255.255', BROADCAST_PORT))
            time.sleep(0.1)
    except:
        traceback.print_exc()
    s.close()
    
thread = threading.Thread(target = broadcast)
thread.start()


def behandle_spieler_verbindung(verbindung):
    try:
        stdio.set_socket(verbindung)
        sys.stderr.write( 'habe verbindung angenommen!\n')
        print 'Hallo! :)'
        while 1:
            weiter_in('start')
    finally:
        verbindung.close()

################ Held

verbindungsinformationen = threading.local()

class Held(object):
    pass

def held():
    if hasattr(verbindungsinformationen, 'held'):
        return verbindungsinformationen.held
    else:
        held = Held() # neuer Held!
        verbindungsinformationen.held = held
        return held

class Zimmer(object):
    def __init__(self, name):
        self.name = name
    
alle_zimmer = {} # Zimmername -> zimmer

def zimmer(name):
    if not name in alle_zimmer:
        alle_zimmer.setdefault(name, Zimmer(name))
    return alle_zimmer[name]
        
def weiter_im(zimmer):
    # datei finden
    dateiname = zimmer + '.py'
    if not os.path.isfile(dateiname):
        print 'Doch das Zimmer', zimmer, 'gibt es hier nicht!'
        return 'Das Zimmer gibt es nicht.'
    # datei ausfuehren
    try:
        execfile( dateiname )
        return 'Fertig durch das Zimmer gelaufen.'
    except SyntaxError:
        traceback.print_exc(file = sys.stdout)
        print "Das Zimmer", zimmer ,"wird gerade renoviert. Es hat noch diesen Fehler, weshalb man es nicht betreten kann"
        return 'SyntaxError'
    except:
        traceback.print_exc(file = sys.stdout)
        print "Als du in dem Zimmer warst, ist der Fehler von obendrüber aufgetreten. "
        print "Das hat dich dorthin zurück katapultiert, wo du vorher warst."
        return 'Fehler'


weiter_in = weiter_im

rechnername = socket.gethostname()

__all__ = ['weiter_in', 'weiter_im', 'held', 'rechnername', 'zimmer']


if __name__ == '__main__':
    while 1:
        print '-' * 80
        weiter_in('start')