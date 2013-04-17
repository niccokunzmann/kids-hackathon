# -*- coding: utf-8 -*-
from spiel import *

ich = held()
print '-' * 80
print 'Willkommen im Schloss', rechnername
print 'Wie heisst du?'
ich.name = raw_input()

print "Sei Willkommen im Spiel,", ich.name
print "Du gehst ins Wohnzimmer..."
weiter_im('wohnzimmer')
print "du bist zurück vom Wohnzimmer"
