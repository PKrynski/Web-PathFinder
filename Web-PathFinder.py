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
    {'id': 'BIA', 'name': 'Białystok'},
    {'id': 'BZG', 'name': 'Bydgoszcz'},
    {'id': 'CZE', 'name': 'Częstochowa'},
    {'id': 'ELK', 'name': 'Ełk'},
    {'id': 'GDN', 'name': 'Gdańsk'},
    {'id': 'KTW', 'name': 'Katowice'},
    {'id': 'KIE', 'name': 'Kielce'},
    {'id': 'KOS', 'name': 'Koszalin'},
    {'id': 'KRK', 'name': 'Kraków'},
    {'id': 'LUB', 'name': 'Lublin'},
    {'id': 'LCJ', 'name': 'Łódź'},
    {'id': 'OLS', 'name': 'Olsztyn'},
    {'id': 'OPO', 'name': 'Opole'},
    {'id': 'POZ', 'name': 'Poznań'},
    {'id': 'RAD', 'name': 'Radom'},
    {'id': 'WAW', 'name': 'Warszawa'},
    {'id': 'WRO', 'name': 'Wrocław'},
    {'id': 'SZZ', 'name': 'Szczecin'}
]

my_map = WorldMap()
for city in cities:
    for key in city:
        if key == "id":
            print city[key]
            my_map.add_city(city[key])

# for city in cities:
#    my_map.add_city(city)

my_map.add_path('WAW', 'BIA', 197)
my_map.add_path('WAW', 'OLS', 214)
my_map.add_path('WAW', 'LCJ', 130)
my_map.add_path('WAW', 'RAD', 104)
my_map.add_path('RAD', 'LUB', 116)
my_map.add_path('RAD', 'KIE', 78)
my_map.add_path('KIE', 'KRK', 116)
my_map.add_path('KRK', 'KTW', 78)
my_map.add_path('KTW', 'CZE', 74)
my_map.add_path('CZE', 'LCJ', 124)
my_map.add_path('KTW', 'OPO', 108)
my_map.add_path('OPO', 'WRO', 94)
my_map.add_path('WRO', 'POZ', 173)
my_map.add_path('POZ', 'LCJ', 218)
my_map.add_path('POZ', 'SZZ', 264)
my_map.add_path('POZ', 'BZG', 142)
my_map.add_path('SZZ', 'BZG', 257)
my_map.add_path('SZZ', 'KOS', 161)
my_map.add_path('KOS', 'GDN', 187)
my_map.add_path('GDN', 'BZG', 167)
my_map.add_path('GDN', 'OLS', 160)
my_map.add_path('OLS', 'ELK', 153)
my_map.add_path('ELK', 'BIA', 107)
my_map.add_path('BIA', 'LUB', 246)
my_map.add_path('BZG', 'LCJ', 217)

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

