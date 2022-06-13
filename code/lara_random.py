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

    
    load(file_stations, file_connections)
