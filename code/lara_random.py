"""
random algoritm (klad bestand)
"""

# add the 'code' directory to the path to use functions from load.py
import os, sys
from re import I
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, 'code'))

from load import *

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

