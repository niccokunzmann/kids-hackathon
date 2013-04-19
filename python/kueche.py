# -*- coding: utf-8 -*-

from spiel import *

ich = held()
raum = zimmer('küche')

if not hasattr(raum, 'helden'):
    raum.helden = []

raum.helden.append(ich)
if raum.helden:
    print "Im Raum sind",
    for held in raum.helden:
        print held.name,
    print '.'

raw_input()
raum.helden.remove(ich)
