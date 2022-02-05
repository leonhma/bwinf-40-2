from citymap2 import CityMap
from os import path


print('--------------------------------------------------------------------------------')
print('A1: Müllabfuhr')
print('Geben sie die Nummer des Beispiels ein ([0; 8])')

path = path.join(
    path.dirname(path.realpath(__file__)), 'beispieldaten', f'muellabfuhr{0}.txt'
)

def print_citymap(citymap: CityMap):
    print('--------------------------------------------------------------------------------')
    print('Printing CityMap')
    print('Nodes:')
    for node in citymap.nodes:
        print(f'{node.id}: {[citymap.get_other_node(node, r).id for r in node.connected_roads]}')
    print('--------------------------------------------------------------------------------')


with open(path, 'r') as f:
    data = f.read()
citymap = CityMap(data.split('\n'))
print_citymap(citymap)
average_daily_way = citymap.get_average_daily_way()
paths = {'Montag': [], 'Dienstag': [], 'Mittwoch': [], 'Donnerstag': [], 'Freitag': []}
for day in paths:
    citymap.set_gravity_towards_home(False)
    paths[day] = [citymap.nodes[0].id]  # log the path it took that day
    road = citymap.get_next_road(citymap.nodes[0])
    next_node = citymap.go_down_road(citymap.nodes[0], road)
    paths[day] += [next_node.id]
    driven = road.length
    for _ in range(50):
        if driven > average_daily_way/2:
            citymap.set_gravity_towards_home(True)
        road = citymap.get_next_road(next_node)
        next_node = citymap.go_down_road(next_node, road)
        paths[day] += [next_node.id]
        if next_node.id == 0:
            break
        driven += road.length
print(paths)



