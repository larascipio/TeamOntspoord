"""
random algoritm (klad bestand)
"""

# add the 'code' directory to the path to use functions from load.py
import os, sys
from re import I

from matplotlib.pyplot import connect
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, 'code'))

from load import *
from bad_algorithm import *
from output import *
from change_connections import *

def start_route(stations): 
    list_stations = list(stations.items())
    station = random.choice(list_stations)
    print(station)
    station[1]._passed = True 
    return station

def random_route(station):
    distance_route = 0
    possible_connections = []
    route = [first_station]
    while distance_route <= 120:
        for connection in station[1]._connections:
            if connection._passed is False:
                possible_connections.append(connection)
        connection = random.choice(possible_connections)
        connection._passed = True 
        connection._stations[1]._passed = True
        route.append(connection._stations[1])
        distance_route += connection._distance
    print(route)
    return route 


if __name__ == '__main__':
    file_stations = './data/StationsNationaal.csv'
    file_connections = './data/ConnectiesNationaal.csv'

    stations = load(file_stations, file_connections)

    # Return random station to start route 
    first_station = start_route(stations)

    # Return a random route 
    random_route(first_station)

        # get connection with shortest distance
        # shortest = 63
        # for connection in start_station[1]._connections:
        #     if connection._distance < shortest:
        #         shortest  = connection._distance
        #         shortest_connection = connection
        # choose random connection
    	
        # connection = random.choice(station[1]._connections)
        # if connection._passed == False:
        #     connection._passed = True
        # else:
        #     connection = random.choice(station[1]._connections)
        # station = connection._stations[1]
        
        # distance_route += connection._distance
        # print(distance_route)
