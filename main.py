"""
main.py
"""
import os, sys
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, 'code'))

from load import *

if __name__ == '__main__':
    file_stations = './data/StationsHolland.csv'
    file_connections = './data/ConnectiesHolland.csv'
    stations = load(file_stations, file_connections)
    print_stationdictionary(stations)