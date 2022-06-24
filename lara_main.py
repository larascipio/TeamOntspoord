"""
main.py
"""
from code.algorithms.random_algorithm import Make_Random_Routes
from code.algorithms.lara_algorithm import Depth_First
from code.visualisation.plotly_animation import create_animation
from code.classes.structure import Railnet
from code.visualisation.quality_hist import quality_hist
from code.visualisation.output import output
import argparse

if __name__ == '__main__':

    # use commandline arguments to choose the railroad
    parser = argparse.ArgumentParser(description='create routes')
    parser.add_argument("type", choices=['holland','national'], help="Use the holland or national railroads")
    parser.add_argument("runs", type=int, nargs="?", default=10000, help="Amount of runs")
    parser.add_argument("algorithm", choices=['random','new'], default='random', help="Random, bad or hillclimber algrorithm")

    args = parser.parse_args()

    if args.type == 'holland':
        file_stations = 'data/StationsHolland.csv'
        file_connections = 'data/ConnectiesHolland.csv'
        max_trains = 7
        max_time = 120
    else:
        file_stations = 'data/StationsNationaal.csv'
        file_connections = 'data/ConnectiesNationaal.csv'
        max_trains = 20
        max_time = 180
    
    qualityroutes = []
    best_quality = 0
    rails = Railnet()
    rails.load(file_stations, file_connections)

    if args.algorithm == 'random':
        for _ in range(args.runs):
            route = Make_Random_Routes(rails, max_trains, max_time)
            route.run()
            quality = route.quality()

            if quality > best_quality:
                    best_quality = quality
                    best_route = route
                    print(best_route)


            qualityroutes.append(quality)
            rails.reset()

    if args.algorithm == 'new':
        for _ in range(args.runs):
            route = Depth_First(rails)
            route.run()
            quality = route.quality()

            if quality > best_quality:
                best_quality = quality
                best_route = route
                print(best_route)

            qualityroutes.append(best_quality)
            rails.reset()

    quality_hist(qualityroutes)
    output(best_quality, best_route.get_trains(), 'output.csv')
    rails.follow_track(best_route.get_trains())

    choose_plot = input('Do you want a detailed visualisation of the route? (y/n) ')


    # for _ in range(100):
    #     route = Make_Bad_Routes(rails, max_trains, max_time) # TODO dit moet het random-algoritme worden
    #     route.run()
    #     qualityroutes[quality] = route
    #     rails.reset()
    
    # # Create hist for best routes 
    # quality_hist(qualityroutes)

        # create_animation(list(stationdict.values()), connectionlist, route)
    

        # quality, route = make_bad_routes(list(stationdictionary.values()), connectionlist, 7, 120)

        # qualityroutes[quality] = route
        # for connection in connectionlist:
        #     print(connection._passed)
    
    # # Create hist for best routes 
    # quality_hist(qualityroutes)


    # """
# random algoritm (klad bestand)
# """

# import random

# def get_available_connections(stations):
#     available_connections = []
#     for station in stations:
#         for connection in stations[station]._connections:
#             if connection._passed is False:
#                 available_connections.append(connection)
#     return available_connections

# def random_route(connections):
#      # Select a connection
#     connection = random.choice(connections)
    
#     # First station passed 
#     connection._stations[1]._passed = True
#     connection._passed = True 
    
#     distance_route = 0
#     route = [connection._stations[1]]

#     while distance_route <= 120:
#         possible_connections = get_available_connections(connections)
#         for connection in connection._stations[1]._connections:
#             if connection._passed is False:
#                 possible_connections.append(connection)
    
#         connection = random.choice(possible_connections) 
#         connection._stations[1]._passed = True
#         connection._passed = True
#         route.append(connection._stations[1])
#         distance_route += connection._distance
#     print(route)
#     return route 

# def passed_connections(connections):
#     pass

# def passed_station(self):
#     pass

# if __name__ == '__main__':
#     file_stations = './data/StationsNationaal.csv'
#     file_connections = './data/ConnectiesNationaal.csv'

#     stations = load(file_stations, file_connections)

#     # Get all non-passed connections
#     available_connections = get_available_connections(stations)
    
#     # Start route with a random connection
#     route = random_route(available_connections)

#     # Check if all connections are passed 
#     passed_connections

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