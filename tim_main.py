"""
tim_main.py
"""

from code.algorithms.bad_algorithm import Make_Greedy_Routes
from code.algorithms.random_algorithm import Make_Random_Routes
from code.algorithms.simulated_annealing import Hillclimber, Simulated_Annealing
from code.algorithms.random_iteration import Make_Iterated_Routes
from code.algorithms.biased_iteration import Make_Biased_Routes
from code.classes.structure import Railnet
# from code.visualisation.quality_hist import quality_hist
from code.visualisation.output import output
from code.visualisation.simple_visualization import simple_visualization
from code.visualisation.plotly_animation import create_animation
from tim_quality_hist import quality_hist
import argparse


if __name__ == '__main__':

    # Use commandline arguments to choose the railroad, algorithm, amount of runs/changed connections and a failed station
    # Amount of runs, changing connections or having a failed station is optional
    parser = argparse.ArgumentParser(description='create routes')
    parser.add_argument("type", choices=['holland','national'], default='holland', help="Use the holland or national railroads")
    parser.add_argument("algorithm", choices=['random','bad','hillclimber', 'iteration', 'annealing', 'bias'], default='random', help="Choose algrorithm")
    parser.add_argument("runs", type=int, nargs="?", default=1, help="Amount of runs")
    parser.add_argument("changeconnection", type=int, nargs="?", default=0, help="Amount of changed connections")
    parser.add_argument("stationfailure", nargs="?", help="Give failed station")
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

    # Loads the railnet
    rails = Railnet(max_trains, max_time)
    rails.load(file_stations, file_connections)

    # Failed station if desired
    if args.stationfailure:
        rails.station_failure(args.stationfailure)
        rails.remove_unconnected_stations()

    # Change a number of random connections of choice
    for _ in range(args.changeconnection):
        rails.change_connection()
    
    # Choose the algorithm
    if args.algorithm == 'random':
        Algorithm = Make_Random_Routes
    elif args.algorithm == 'bad':
        Algorithm = Make_Greedy_Routes
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
        print(i)
    
    if best_quality > 0:
        output(best_quality, best_route, 'output.csv')

    if args.runs > 1:
        quality_hist(qualityroutes)

    choose_plot = input('Do you want a detailed visualisation of the route? (y/n) ')

    if choose_plot == "y":
        rails.restore_routes(best_route)
        create_animation(rails)
    else:
        # Simple visualisation
        rails.restore_routes(best_route)
        simple_visualization(rails)
