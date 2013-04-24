# -*- coding: utf-8 -*-
from spiel import *

ich = held()
print '-' * 80
print 'Willkommen im Schloss', rechnername
print 'Wie heißt du?'
ich.name = raw_input()
print 'Ich grüße dich,', ich.name
weiter_im('keller')
