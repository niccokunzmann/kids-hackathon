from spiel import *

print('du bist in der Wohnung')

s = ''
if raw_input('ansehen(j/N)') == 'j':
    print('Hier gibt es Vier Stühle, die um einen Tisch stehen, der aus Kiefernholz gefertigt ist.')
    #print('es sitzen dort:')
    if raw_input('hinsetzen(j/N)') == 'j':
        print('der stuhl macht bedrohliche geräusche unter deinem gewicht')
        print('leise fallen stückchen von ihm ab, die garnicht gutes vermuten '
              'lassen, was die Zukunft dieses Stuhles betrifft')
        for i in range(3):
            s = raw_input('du sprichst zu dir selbst:')
            print(s)

print('nach einer weile wird es dir langweilig und du magst die kücher verlassen.')
raw_input()
print('es ist so langweilig dort, dass du anfängst zu gähnen')
print('du denkst dir eine Zahl:')
z = raw_input('')
print(z * 2 + 'Fledermäuse umfliegen dich und spucen dir in den mund.')
if raw_input('Wird dir schlecht? (ja./nein.)') == 'ja.':
    print('du rennst in die Küche')
    du.geschmack = 'gut'
    gehe_zu('küche')
else:
    print('Das lässt vermuten, dass du manchmal sehr merkwürdige Sachen isst!')
    du.geschmack = 'schlecht'


        
        
    
