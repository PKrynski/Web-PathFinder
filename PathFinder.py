# -*- coding: utf-8 -*-
from collections import defaultdict, deque

class WorldMap(object):
    def __init__(self):
        self.cities = set()
        self.neighbours = defaultdict(list)
        self.distances = {}

    def add_city(self, value):
        self.cities.add(value)

    def add_path(self, from_city, to_city, distance):
        self.neighbours[from_city].append(to_city)
        self.neighbours[to_city].append(from_city)          # for two-way city connections
        self.distances[(from_city, to_city)] = distance
        self.distances[(to_city, from_city)] = distance     # for two-way city connections


def calculatePaths(map_data, start):
    visited = {start: 0}
    path = {}

    cities = set(map_data.cities)

    while cities:
        previous = None
        for city in cities:
            if city in visited:
                if previous is None:
                    previous = city
                elif visited[city] < visited[previous]:
                    previous = city
        if previous is None:
            break

        cities.remove(previous)
        current_weight = visited[previous]

        for current_city in map_data.neighbours[previous]:
            try:
                weight = current_weight + map_data.distances[(previous, current_city)]
            except KeyError:
                continue                    # no connection -> check next city

            if current_city not in visited or weight < visited[current_city]:
                visited[current_city] = weight
                path[current_city] = previous

    return visited, path


def getShortestPath(the_map, start, destination):
    visited, paths = calculatePaths(the_map, start)
    full_path = deque()

    try:
        current_target = paths[destination]
    except KeyError:
        print "Taka droga nie istnieje!"
        return

    while current_target != start:
        full_path.appendleft(current_target)
        current_target = paths[current_target]

    full_path.appendleft(start)
    full_path.append(destination)

    return list(full_path), visited[destination]

if __name__ == '__main__':
    my_map = WorldMap()

    city_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    for city in city_list:
        my_map.add_city(city)

    my_map.add_path('A', 'B', 22)
    my_map.add_path('A', 'C', 24)
    my_map.add_path('B', 'D', 13)
    my_map.add_path('C', 'D', 39)
    my_map.add_path('B', 'E', 48)
    my_map.add_path('D', 'E', 27)
    my_map.add_path('E', 'F', 5)
    my_map.add_path('F', 'G', 2)

    best_path, weight = getShortestPath(my_map, "G", "A")

    print "Najlepsza droga: ", best_path
    print "Waga połączenia: %d" % weight