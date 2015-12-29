# -*- coding: utf-8 -*-
from collections import defaultdict, deque
from flask import Flask, render_template, request, abort, make_response
from uuid import uuid4
import json

app_url = '/krynskip/nav'
app = Flask(__name__)

# Odkomentuj, jeśli potrzebujesz debuggera
from werkzeug.debug import DebuggedApplication

app.debug = True
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

cities = [
    {'id': 'WAW', 'name': 'Warszawa'},
    {'id': 'PNO', 'name': 'Piaseczno'},
    {'id': 'KRK', 'name': 'Kraków'},
    {'id': 'GDN', 'name': 'Gdańsk'},
    {'id': 'POZ', 'name': 'Poznań'},
    {'id': 'BZG', 'name': 'Bydgoszcz'},
    {'id': 'SZZ', 'name': 'Szczecin'},
    {'id': 'KTW', 'name': 'Katowice'},
]

routes = []

#begin pathfinder code

class WorldMap(object):
    def __init__(self):
        self.cities = set()
        self.neighbours = defaultdict(list)
        self.distances = {}

    def add_city(self, value):
        self.cities.add(value)

    def add_path(self, from_city, to_city, distance):
        self.neighbours[from_city].append(to_city)
        self.neighbours[to_city].append(from_city)  # for two-way city connections
        self.distances[(from_city, to_city)] = distance
        self.distances[(to_city, from_city)] = distance  # for two-way city connections


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
                continue  # no connection -> check next city

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

#end pathfinder code

@app.route('/')
def hello_world():
    return 'Welcome to the PathFinder app!'

#@app.route(app_url + '/cities', methods=['GET'])
#def get_cities():
#    return json.dumps(cities)


#@app.route(app_url + '/cities', methods=['POST'])
#def add_city():
#    data = request.get_data()
#    try:
#        city = json.loads(data)
#        if city.get('name') is None:
#            abort(400)
#        if city.get('id') is None:
#            abort(400)
#        cities.append(city)
#        return json.dumps({"status": "OK", "msg": "Dodano nowe miasto"})
#    except ValueError, e:
#        abort(400)


@app.route(app_url + '/routes', methods=['GET','POST'])
def create_new_route():

    print "TUTAJ JEST"

    if request.method == 'GET':
        print "GET METHOD"

        start = request.args['from']
        end = request.args['to']

        print "Start: " + start
        print "End: " + end

        best_route, distance = getShortestPath(my_map, "KTW", "WAW")

        new_route = {"id": str(uuid4()), "route": best_route, "weight": distance}
        routes.append(new_route)

        response = make_response()
        response.headers['Location'] = app_url + '/r/' + new_route['id']
        return response

    if request.method == 'POST':

        data = request.get_data()
        try:
            arguments = json.loads(data)
            if arguments.get('from') is None:
                abort(400)
            if arguments.get('to') is None:
                abort(400)
            import time
            time.sleep(3)

            print "Start: " + arguments.get('from')
            print "End: " + arguments.get('to')

            best_route, distance = getShortestPath(my_map, "KTW", "WAW")

            new_route = {"id": str(uuid4()), "route": best_route, "weight": distance}
            routes.append(new_route)

            response = make_response()
            response.headers['Location'] = app_url + '/r/' + new_route['id']
            # json.dumps({"status":"OK", "msg":"Wyliczono trasę"})
            return response
        except ValueError, e:
            abort(400)


@app.route(app_url + '/r/<uid>')
def get_route(uid):

    print routes

    for route_item in routes:
        for key in route_item:
            if key == "id":
                if route_item[key] == uid:
                    return json.dumps(route_item['route'])

    if uid in routes:
        return json.dumps(routes[uid])

    return "Przykro mi, ale trasa: " + uid + " nie istnieje :("

if __name__ == '__main__':
    my_map = WorldMap()

    # cities = ['WAW', 'PNO', 'KRK', 'GDN', 'POZ', 'SZZ', 'KTW']

    for city in cities:
        for key in city:
            if key == "id":
                print city[key]
                my_map.add_city(city[key])

    # for city in cities:
    #    my_map.add_city(city)

    my_map.add_path('WAW', 'PNO', 22)
    my_map.add_path('WAW', 'KRK', 24)
    my_map.add_path('PNO', 'GDN', 13)
    my_map.add_path('KRK', 'GDN', 39)
    my_map.add_path('PNO', 'POZ', 48)
    my_map.add_path('GDN', 'POZ', 27)
    my_map.add_path('POZ', 'SZZ', 5)
    my_map.add_path('SZZ', 'KTW', 2)

    best_path, weight = getShortestPath(my_map, "KTW", "WAW")

    print "Najlepsza droga: ", best_path
    print "Waga połączenia: %d" % weight

    app.run()
