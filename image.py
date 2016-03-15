

img = open('rubber-duck-small.png', 'rb')

for b in img:
    print('line -> ', b.decode('ISO-8859-1'))
