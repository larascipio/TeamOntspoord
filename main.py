"""
main.py
"""
from code.classes.load import load, print_stationdictionary
from code.algorithms.bad_algorithm import make_bad_routes
from code.visualisation.quality_hist import quality_hist
# from code.classes.change_connections import *
# from code.visualisation.simple_visualization import *
import argparse

def reset_model(stationdictionary, connectionlist):
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
        file_stations = 'data/StationsHolland.csv'
        file_connections = 'data/ConnectiesHolland.csv'
        max_trains = 7
        max_time = 120
    else:
        file_station = 'data/StationsNationaal.csv'
        file_connections = 'data/ConnectiesNationaal.csv'
        max_trains = 20
        max_time = 180
    
    stations = load(file_stations, file_connections)
    
    qualityroutes = {}
    stationdictionary, connectionlist = load(file_stations, file_connections)
    
    for _ in range(1):
        quality, route = make_bad_routes(list(stationdictionary.values()), 7, 120, 28)
        # TODO overwrite sommige dictionary entries
        qualityroutes[quality] = route
        # for connection in connectionlist:
        #     print(connection._passed)

        reset_model(stationdictionary, connectionlist)
    
    # Create hist for best routes 
    quality_hist(qualityroutes)



