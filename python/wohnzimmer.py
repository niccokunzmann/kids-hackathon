# -*- coding: utf-8 -*-

from spiel import *

ich = held()

print 'Du bist im Wohnzimmer'

# mehr zu point and click umbauen
# spiel bringt python bei
# tasse heißer schwarzer tee

s = ''
if raw_input('ansehen(j/N)') == 'j':
    print 'Hier gibt es Vier Stühle, die um einen Tisch stehen, der aus Kiefernholz gefertigt ist.'
    #print 'es sitzen dort:')
    if raw_input('hinsetzen(j/N)') == 'j':
        print 'der stuhl macht bedrohliche geräusche unter deinem gewicht'
        print 'leise fallen stückchen von ihm ab, die gar nichts gutes vermuten ' \
              'lassen, was die Zukunft dieses Stuhles betrifft'
        for i in range(3):
            s = raw_input('du sprichst zu dir selbst:')
            print s

print 'nach einer weile wird es dir langweilig und du magst die wohnung verlassen.' 
raw_input()
print 'es ist so langweilig dort, dass du anfängst zu gähnen' 
print 'du denkst dir eine Zahl:' 
z = raw_input('')
print z * 2, 'Fledermäuse umfliegen dich und spucken dir in den Mund.'
if raw_input('Wird dir schlecht? (ja./nein.)') == 'ja.':
    print 'Nach dem Schrecken rennst du in die Küche.'
    ich.geschmack = 'gut'
    weiter_in('küche')
else:
    print 'Das lässt vermuten, dass du manchmal sehr merkwürdige Sachen isst!'
    ich.geschmack = 'schlecht'