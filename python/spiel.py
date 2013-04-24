#!/usr/bin/python2
import pickle
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
            if self.socket:
                self.socket.sendall(string)
            else:
                self.stdout.write(string)
            #sys.stderr.write('schreibe: ' + str(string))
            #self.flush_stdout()
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
thread.daemon = True
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
thread.daemon = True
thread.start()



def behandle_spieler_verbindung(verbindung):
    try:
        stdio.set_socket(verbindung)
        main()
    finally:
        verbindung.close()

################ Speichern

alle_spielstaende = {} # (class, name) -> obj

SPEICHERINTERVALL = 1 # Sekunden
_zu_speichern = []

def alles_abspeichern():
    while 1:
        for stand in _zu_speichern:
            try:
                stand.speichern()
            except:
                traceback.print_exc()
        time.sleep(SPEICHERINTERVALL)
    
thread = threading.Thread(target = alles_abspeichern)
thread.daemon = True
thread.start()
            
def wird_gespeichert(spielstand):
    _zu_speichern.append(spielstand)

def lade_spielstand(cls, name):
    stand = alle_spielstaende.get((cls, name))
    print 'lade_spielstand', alle_spielstaende
    if stand is None: stand = cls(name)
    return stand
    
class Spielstand(object):
    _speichernd = [] # welche objekte werden gerade abgespeichert
    _speicherzeit = 0
    _name = None
    
    def __init__(self, name = None):
        self.name = name
        
    @property
    def name(self):
        return self._name
        
    @name.setter
    def name(self, name):
        if name is None:
            return 
        print 'setze name von', self._name, 'zu', name
        if self._name is None:
            self._name = name
            self.laden()
            wird_gespeichert(self)
        elif self.name == name: pass
        else: print "Wie kommt es,", self._name, ", dass sie einen " \
                    "anderen Namen wie'", name, "'annehmen wollen?"

    def datei_name(self):
        if not os.path.isdir('spielstand'):
            os.mkdir('spielstand')
        return os.path.join('spielstand', self.name + '.' + \
                                 self.__class__.__name__.lower())
        
    def wird_gespeichert(self):
        return (self, threading._get_ident()) in self._speichernd
    
    def speichern(self):
        self._speichernd.append((self, threading._get_ident()))
        try:
            with open(self.datei_name(), 'wb') as f:
                pickle.dump(self, f)
        finally:
            self._speichernd.remove((self, threading._get_ident()))
            
    def __reduce__(self):
        if not self.wird_gespeichert():
            return lade_spielstand, (self.__class__, self.name)
        return lade_spielstand, (self.__class__, self.name), self.__dict__
        
    def laden(self):
        print 'laden..'
        if not os.path.isfile(self.datei_name()):
            return 
        assert alle_spielstaende.get((self.__class__, self.name)) is None, \
               alle_spielstaende.get((self.__class__, self.name))
        alle_spielstaende[(self.__class__, self.name)] = self
        print 'laden!'
        with open(self.datei_name(), 'rb') as f:
                pickle.load(f)

################ Held
                
verbindungsinformationen = threading.local()

class Held(Spielstand):
    pass

def held():
    if hasattr(verbindungsinformationen, 'held'):
        return verbindungsinformationen.held
    else:
        held = Held() # neuer Held!
        verbindungsinformationen.held = held
        return held

class Zimmer(Spielstand):
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
        print "Das Zimmer", zimmer ,"wird gerade renoviert. Es hat noch diesen"\
              " Fehler, weshalb man es nicht betreten kann"
        return 'SyntaxError'
    except:
        traceback.print_exc(file = sys.stdout)
        print "Als du in dem Zimmer warst, ist der Fehler von obendrüber " \
              "aufgetreten. "
        print "Das hat dich dorthin zurück katapultiert, wo du vorher warst."
        return 'Fehler'


weiter_in = weiter_im

rechnername = socket.gethostname()

alle_helden = []

def main():
    _held = held()
    alle_helden.append(_held)
    try:
        while 1:
            s = weiter_in('start')
            if s != 'Fertig durch das Zimmer gelaufen.':
                print s
                break    
    finally:
        if _held in alle_helden:
            alle_helden.remove(_held)

verbindungsname = '%s:%i' % (rechnername, PORT_VERBINDUNG)
            
__all__ = ['weiter_in', 'weiter_im', 'held', 'rechnername', 'zimmer', \
           'lade_spielstand', 'main', 'alle_helden', 'verbindungsname', \
           'PORT_VERBINDUNG']

if __name__ == '__main__':
    print 'Beim verbinden muss das eingegeben werden: %s' % (verbindungsname,) 
    main()
