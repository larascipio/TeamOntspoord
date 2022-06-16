"""
tim_main.py
"""

from code.algorithms.bad_algorithm import Make_Bad_Routes
from code.algorithms.random_algorithm import Make_Random_Routes
from code.algorithms.simulated_annealing import Hillclimber
from code.visualisation.plotly_animation import create_animation
from code.classes.structure import Railnet
from code.visualisation.quality_hist import quality_hist
from code.visualisation.output import output
from code.visualisation.simple_visualization import simple_visualization
import argparse

if __name__ == '__main__':

    # use commandline arguments to choose the railroad, algorithm, amount of runs and changed connections and a failed station
    parser = argparse.ArgumentParser(description='create routes')
    parser.add_argument("type", choices=['holland','national'], default='holland', help="Use the holland or national railroads")
    parser.add_argument("algorithm", choices=['random','bad','hillclimber'], default='random', help="Random, bad or hillclimber algrorithm")
    parser.add_argument("runs", type=int, default=1, help="Amount of runs")
    parser.add_argument("changeconnection", nargs="?", type=int, default=1, help="Amount of changed connections")
    parser.add_argument("stationfailure", nargs="?", help="give failed station")
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

    # runs = int(input('How many times do you want to run this? '))
    # failed_station = input('Which station should fail? If not valid, none will fail. ')
    # changed_connection = input('Change a connection? y/n ')
    qualityroutes = []
    best_quality = 0
    rails = Railnet()
    rails.load(file_stations, file_connections)
    rails.station_failure(args.stationfailure)
    for _ in range(args.changeconnection):
        rails.change_connection()

    for _ in range(args.runs):
        route = Make_Random_Routes(rails, max_trains, max_time)
        route.run()
        route_quality = route.quality()
        if route_quality > best_quality:
           best_quality = route_quality
           best_route = route

        qualityroutes.append(route_quality)
        rails.reset()
    
    quality_hist(qualityroutes, best_quality, best_route)
    rails.follow_track(best_route.get_trains())
    simple_visualization(rails._stations, list(rails._connections.values()))
    create_animation(rails, best_route)

    
