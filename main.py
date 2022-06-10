"""
main.py
"""

# add the 'code' directory to the path to use functions from load.py
import os, sys
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, 'code'))

from load import *
from bad_algorithm import *

if __name__ == '__main__':
    file_stations = './data/StationsNationaal.csv'
    file_connections = './data/ConnectiesNationaal.csv'

    qualityroutes = {}
    for _ in range(100):
        stations = load(file_stations, file_connections)
        # print_stationdictionary(stations)
        stationlist = list(stations.values())
        quality, route = make_bad_routes(stationlist, 20, 180)
        qualityroutes[quality] = route
    
    # the best route
    highest = max(qualityroutes)
    print(max(qualityroutes.keys()))
    best_route = qualityroutes[highest]
    print('The best route is:')
    for train in best_route:
        print(train._route)
    print(f'with a quality of {highest}')