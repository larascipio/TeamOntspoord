"""
tim_main.py
"""

from code.algorithms.bad_algorithm import Make_Bad_Routes
from code.algorithms.random_algorithm import Make_Random_Routes
from code.algorithms.simulated_annealing import Hillclimber
from code.algorithms.self_choosing import Make_Iterated_Routes
from code.visualisation.plotly_animation import create_animation
from code.classes.structure import Railnet
from code.visualisation.quality_hist import quality_hist
from code.visualisation.output import output
from code.visualisation.simple_visualization import simple_visualization
import argparse


if __name__ == '__main__':

    # Use commandline arguments to choose the railroad, algorithm, amount of runs/changed connections and a failed station
    # Amount of runs, changing connections or having a failed station is optional
    parser = argparse.ArgumentParser(description='create routes')
    parser.add_argument("type", choices=['holland','national'], default='holland', help="Use the holland or national railroads")
    parser.add_argument("algorithm", choices=['random','bad','hillclimber', 'iteration'], default='random', help="Random, bad or hillclimber algrorithm")
    parser.add_argument("runs", type=int, nargs="?", default=1, help="Amount of runs")
    parser.add_argument("changeconnection", type=int, nargs="?", default=0, help="Amount of changed connections")
    parser.add_argument("stationfailure", nargs="?", help="Give failed station")
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

    # Loads the objects and variables used for visualisation. 
    qualityroutes = []
    best_quality = 0
    rails = Railnet()
    rails.load(file_stations, file_connections)
    rails.station_failure(args.stationfailure)

    # Change a number of random connections of choice
    for _ in range(args.changeconnection):
        rails.change_connection()

    # Actually runs the algorithm of choice - put the if-statement outside the loop so the code runs faster
    if args.algorithm == 'random':
        for _ in range(args.runs):

            route = Make_Random_Routes(rails, max_trains, max_time)
            route.run()
            route_quality = route.quality()

            if route_quality > best_quality:
                best_quality = route_quality
                best_route = route

            qualityroutes.append(route_quality)
            rails.reset()

    elif args.algorithm == "bad":
        for _ in range(args.runs):

            route = Make_Bad_Routes(rails, max_trains, max_time)
            route.run()
            route_quality = route.quality()

            if route_quality > best_quality:
                best_quality = route_quality
                best_route = route

            qualityroutes.append(route_quality)
            rails.reset()

    # TODO Hillclimber werkt nog niet - moet iterations toevoegen aan run
    elif args.algorithm == "hillclimber":
        iterations = int(input('How many iterations?'))
        for _ in range(args.runs):

            route = Hillclimber(rails, max_trains, max_time)
            route.run(iterations)
            route_quality = route.quality()

            if route_quality > best_quality:
                best_quality = route_quality
                best_route = route

            qualityroutes.append(route_quality)
            rails.reset()

    elif args.algorithm == "iteration":
        iterations = int(input('How many iterations?'))
        for _ in range(args.runs):
            
            route = Make_Iterated_Routes(rails, max_trains, max_time)
            route.run(iterations)
            route_quality = route.quality()

            if route_quality > best_quality:
                best_quality = route_quality
                best_route = route

            qualityroutes.append(route_quality)
            rails.reset()

    
    quality_hist(qualityroutes)
    output(best_quality, best_route.get_trains(), 'output.csv')
    rails.follow_track(best_route.get_trains())
    print(route.quality())

    choose_plot = input('Do you want a detailed visualisation of the route? (y/n) ')

    if choose_plot == "y":
        create_animation(rails, best_route)
    else:
        simple_visualization(rails._stations, list(rails._connections.values()))
