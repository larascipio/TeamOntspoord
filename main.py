"""
main.py
"""

# add the 'code' directory to the path to use functions from load.py
import os, sys
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, 'code'))

from load import *
from bad_algorithm import *
from output import *

if __name__ == '__main__':
    file_stations = './data/StationsNationaal.csv'
    file_connections = './data/ConnectiesNationaal.csv'

    qualityroutes = {}
    for _ in range(100):
        load(file_stations, file_connections)
        quality, route = make_bad_routes(list(stationdictionary.values()), 20, 180)
        qualityroutes[quality] = route

    # the best route
    highest = max(qualityroutes)
    output(highest, qualityroutes[highest])
