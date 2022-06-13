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
import random

def get_available_connections(stations):
    available_connections = []
    for station in stations:
        for connection in stations[station]._connections:
            if connection._passed is False:
                available_connections.append(connection)
    return available_connections

def random_route(connections):
     # Select a connection
    connection = random.choice(connections)
    
    # First station passed 
    connection._stations[1]._passed = True
    connection._passed = True 
    
    distance_route = 0
    route = [connection._stations[1]]

    while distance_route <= 120:
        possible_connections = get_available_connections(connections)
        for connection in connection._stations[1]._connections:
            if connection._passed is False:
                possible_connections.append(connection)
    
        connection = random.choice(possible_connections) 
        connection._stations[1]._passed = True
        connection._passed = True
        route.append(connection._stations[1])
        distance_route += connection._distance
    print(route)
    return route 

def passed_connections(connections):
    pass

def passed_station(self):
    pass

if __name__ == '__main__':
    file_stations = './data/StationsNationaal.csv'
    file_connections = './data/ConnectiesNationaal.csv'

    stations = load(file_stations, file_connections)

    # Get all non-passed connections
    available_connections = get_available_connections(stations)
    
    # Start route with a random connection
    route = random_route(available_connections)

    # Check if all connections are passed 
    passed_connections

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
