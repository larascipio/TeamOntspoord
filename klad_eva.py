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
import argparse

if __name__ == '__main__':
    # use commandline arguments to choose the railroad
    parser = argparse.ArgumentParser(description='create routes')
    parser.add_argument("type", choices=['holland','national'], help="Use the holland or national railroads")
    args = parser.parse_args()

    if args.type == 'holland':
        file_stations = './data/StationsHolland.csv'
        file_connections = './data/ConnectiesHolland.csv'
        max_trains = 7
        max_time = 120
    else:
        file_station = './data/StationsNationaal.csv'
        file_connections = './data/ConnectiesNationaal.csv'
        max_trains = 20
        max_time = 180

# ----------------------------- Run once ----------------------------------
    rails = Railnet()
    rails.load(file_stations, file_connections)

    algorithm = Hillclimber(rails, max_trains, max_time)
    algorithm.run(10000)


    # create_animation(rails, route)