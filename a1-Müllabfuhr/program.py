from citymap2 import CityMap
from os import path


print('--------------------------------------------------------------------------------')
print('A1: Müllabfuhr')
print('Geben sie die Nummer des Beispiels ein ([0; 8])')

path = path.join(path.dirname(path.realpath(__file__)), 'beispieldaten', f'muellabfuhr{0}.txt')
with open(path, 'r') as f:
    data = f.read()
citymap = CityMap(data.split('\n'))
print(citymap)
print(citymap.nodes[0])

