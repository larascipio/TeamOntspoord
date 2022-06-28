"""
rnet_changes_main.py

Programmeertheorie - minor programmeren
Lara, Tim, Eva

- Can be used to run any of the algorithms created for the RailNL case.
- Uses command line arguments for choosing the dataset, the algorithm and 
    amount of runs, failed station and amount of changed connections
"""

# ------------------------------- Imports --------------------------------------

from code.algorithms.bad_algorithm import Make_Bad_Routes
from code.algorithms.random_algorithm import Make_Random_Routes
from code.algorithms.simulated_annealing import Hillclimber, Simulated_Annealing
from code.algorithms.random_iteration import Make_Iterated_Routes
from code.algorithms.biased_iteration import Make_Biased_Routes
from code.classes.structure import Railnet
from code.visualisation.output import output
from code.visualisation.plotly_animation import create_animation
from tim_quality_hist import quality_hist
import argparse

# ------------------------------- Imports --------------------------------------

if __name__ == '__main__':

    # Use commandline arguments to choose the railroad and algorithm
    # Amount of runs, changing connections or having a failed station is optional
    parser = argparse.ArgumentParser(description='create routes')
    parser.add_argument(
        "type", 
        choices=['holland','national'], 
        default='holland', 
        help="Use the holland or national railroads"
        )
    parser.add_argument(
        "algorithm", 
        choices=[
            'random',
            'bad',
            'hillclimber', 
            'iteration', 
            'annealing', 
            'bias'], 
            default='random', 
            help="Choose algrorithm"
            )
    parser.add_argument(
        "runs", 
        type=int, 
        nargs="?", 
        default=1, 
        help="Amount of runs"
        )
    parser.add_argument(
        "changeconnection", 
        type=int, nargs="?", 
        default=0, 
        help="Amount of changed connections"
        )
    parser.add_argument(
        "stationfailure", 
        nargs="?", 
        help="Give failed station"
        )
    args = parser.parse_args()

    if args.type == 'holland':
        file_stations = 'data/StationsHolland.csv'
        file_connections = 'data/ConnectiesHolland.csv'
        max_trains = 5
        max_time = 120
    else:
        file_stations = 'data/StationsNationaal.csv'
        file_connections = 'data/ConnectiesNationaal.csv'
        max_trains = 20
        max_time = 180

    # --------------------------- Load in rails --------------------------------
    
    # Loads the railnet
    rails = Railnet(max_trains, max_time)
    rails.load(file_stations, file_connections)

    # Failed station if desired
    if args.stationfailure:
        rails.station_failure(args.stationfailure)

    # Change a number of random connections of choice
    for _ in range(args.changeconnection):
        old_connection, new_connection, removed_station_list = rails.change_connection()
        print(f'{old_connection.get_stations()} to {new_connection.get_stations()}')
    
    # Choose the algorithm
    if args.algorithm == 'random':
        Algorithm = Make_Random_Routes
    elif args.algorithm == 'bad':
        Algorithm = Make_Bad_Routes
    elif args.algorithm == 'hillclimber':
        Algorithm = Hillclimber
    elif args.algorithm == 'annealing':
        Algorithm = Simulated_Annealing
    elif args.algorithm == 'iteration':
        Algorithm = Make_Iterated_Routes
    elif args.algorithm == 'bias':
        Algorithm = Make_Biased_Routes

    # The variables used for the loop
    qualityroutes = []
    best_quality = 0

    # Run the algorithm for the given amount of runs
    for i in range(args.runs):

        route = Algorithm(rails)
        route.run()
        route_quality = rails.quality()

        if route_quality > best_quality:
            best_quality = route_quality
            best_route = rails.get_trains()

        qualityroutes.append(route_quality)
        rails.reset()
        print(f'{i + 1}/{args.runs}', end = "\r")

    print("Finished running")
    
    if best_quality > 0:
        output(best_quality, best_route, 'output.csv')

    if args.runs > 1:
        quality_hist(qualityroutes)

    rails.add_route(best_route)
    create_animation(rails)
