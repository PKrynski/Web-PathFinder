# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, abort, make_response
from uuid import uuid4
import json
from PathFinder import WorldMap, getShortestPath

app_url = '/krynskip/web-pathfinder'
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

my_map = WorldMap()
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
my_map.add_path('BZG', 'WAW', 15)
my_map.add_path('BZG', 'GDN', 25)

routes = []


@app.route(app_url + '/')
def hello_world():
    return 'Welcome to the PathFinder web app!'

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

        try:
            best_route, distance = getShortestPath(my_map, start, end)
        except TypeError:
            abort(400)

        new_route = {"id": str(uuid4()), "route": best_route, "weight": distance}
        routes.append(new_route)

        response = make_response()
        response.headers['Location'] = app_url + '/r/' + new_route['id']
        return response

'''
    if request.method == 'POST':

        print "METHOD POST"

        data = request.get_data()

        print data

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

            try:
                best_route, distance = getShortestPath(my_map, "KTW", "WAW")
            except TypeError:
                abort(400)

            new_route = {"id": str(uuid4()), "route": best_route, "weight": distance}
            routes.append(new_route)

            response = make_response()
            response.headers['Location'] = app_url + '/r/' + new_route['id']
            # json.dumps({"status":"OK", "msg":"Wyliczono trasę"})
            return response
        except ValueError, e:
            abort(400)
'''

@app.route(app_url + '/r/<uid>')
def get_route(uid):

    #print routes

    for route_item in routes:
        for key in route_item:
            if key == "id":
                if route_item[key] == uid:
                    return json.dumps(route_item['route'])

    if uid in routes:
        return json.dumps(routes[uid])

    return "Przykro mi, ale trasa: " + uid + " nie istnieje :("


if __name__ == '__main__':

    # cities = ['WAW', 'PNO', 'KRK', 'GDN', 'POZ', 'SZZ', 'KTW']
    '''
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

    #best_path, weight = getShortestPath(my_map, "KTW", "WAW")

    #print "Najlepsza droga: ", best_path
    #print "Waga połączenia: %d" % weight
    '''
    app.run(host='0.0.0.0')

