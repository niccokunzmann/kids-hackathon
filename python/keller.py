# -*- coding: utf-8 -*-
from spiel import *
# alles hier drüber sogt dafür, dass das Spiel läuft


# In der nächsten Zeile wird dem Spieler etwas geschrieben
print 'Hier ist ein Zwerg im Geschräch.'
print 'Der Zwerg fragt dich: "Wie geht es dir?"'

# In der nächsten Zeile wird der Spieler gefragt mit raw_input()
# und seine Antwort in der Variablen antwort gespeichert
antwort = raw_input()

# In der nächten Zeile wird dem Spieler seine Antwort mitgeteilt
print 'Die antwort ist:', antwort

# vergleiche die Antwort mit bestimmten Antworten:
if antwort == 'gut':
    print 'Zwerg: Schön, dass es dir gut geht.'
if antwort == 'schlecht': print 'Zwerg: Das ist aber schade!'
# Falls du keine Antwort gegeben hast
if antwort == '':
    print 'Zwerg: Du musst schon was sagen!'
# testen, wenn die antwort eine ganz andere ist
# != heisst ungleich (nicht gleich)
if antwort != '' or antwort != 'gut' or antwort != 'schlecht':
    print 'Zwerg: Das ist ja unerwartet!'
    
# einen Streit mit dem Zwerg, den man nur verlieren kann:
antwort = ''
while not antwort == 'ja':
    print 'Zwerg: ich bin besser als du, stimmts?'
    antwort = raw_input()
