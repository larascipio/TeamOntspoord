"""
main.py
"""
from code.classes.load import *
from code.algorithms.bad_algorithm import *
from code.visualisation.output import *
from code.classes.change_connections import *
from code.visualisation.simple_visualization import *
import matplotlib.pyplot as plt
import argparse

def reset_model():
    for station in list(stationdictionary.values()):
        station._passed = False
    for connection in connectionlist:
        connection._passed = False

if __name__ == '__main__':

    # use commandline arguments to choose the railroad
    parser = argparse.ArgumentParser(description='create routes')
    parser.add_argument("type", choices=['holland','national'], help="Use the holland or national railroads")
    args = parser.parse_args()

    if args.type == 'holland':
        file_stations = '../data/StationsHolland.csv'
        file_connections = '../data/ConnectiesHolland.csv'
        max_trains = 7
        max_time = 120
    else:
        file_station = '../data/StationsNationaal.csv'
        file_connections = '../data/ConnectiesNationaal.csv'
        max_trains = 20
        max_time = 180
    
    stations = load(file_stations, file_connections)
    
    qualityroutes = {}
    
    #station_failure('Utrecht Centraal')

    for _ in range(1):
        quality, route = make_bad_routes(list(stationdictionary.values()), 7, 120, 28)
        # TODO overwrite sommige dictionary entries
        qualityroutes[quality] = route
        for connection in connectionlist:
            print(connection._passed)
    
        reset_model()
        
    best_qual = max(qualityroutes.keys())
    best_route = qualityroutes[best_qual]
    
    for train in best_route:
        print(train._route)
    
    output(best_qual, best_route)


