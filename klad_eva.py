# # state space?
# c = 3 # num_connections per station
# s = 61 # num_stations
# m = 10 # max connections per trein
# sum = 0
# for i in range(1,m):
#     # print(sum)
#     # print(pow(c,i)*s/2)
#     sum += pow(c,i)*s
# print('{:e}'.format(sum))
# from code.algorithms.bad_algorithm import make_bad_routes
from code.algorithms.simulated_annealing import Hillclimber
from code.classes.structure import Railnet
from code.visualisation.plotly_animation import create_animation
from code.visualisation.quality_hist import quality_hist
import argparse

if __name__ == '__main__':
    # use commandline arguments to choose the railroad
    parser = argparse.ArgumentParser(description='create routes')
    parser.add_argument(
        "type", 
        choices=['holland','national'], 
        help="Use the holland or national railroads"
    )
    args = parser.parse_args()

    if args.type == 'holland':
        file_stations = './data/StationsHolland.csv'
        file_connections = './data/ConnectiesHolland.csv'
        max_trains = 7
        max_time = 120
        iterations = 10000
    else:
        file_stations = './data/StationsNationaal.csv'
        file_connections = './data/ConnectiesNationaal.csv'
        max_trains = 20
        max_time = 180
        iterations = 10000

    # ----------------------------- Run once ----------------------------------
    
    rails = Railnet()
    rails.load(file_stations, file_connections)

    algorithm = Hillclimber(rails, max_trains, max_time)
    algorithm.run(iterations)

    trains = algorithm.get_trains()
    print(len(trains))
    print([train.get_distance() for train in trains])


    # create_animation(rails, algorithm)

    # ----------------------------- Create hist -------------------------------
    hillclimber_qualities = []
    for _ in range(100):
        rails.reset()
        route = Hillclimber(rails, max_trains, max_time)
        route.run(iterations)
        route_quality = route.quality()
        hillclimber_qualities.append(route_quality)
        
    
    # Create hist for best routes 
    quality_hist(hillclimber_qualities)