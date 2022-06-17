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
from code.algorithms.bad_algorithm import make_bad_routes
from code.classes.load import load
from code.visualisation.plotly_animation import create_animation

file_stations = '../data/StationsHolland.csv'
file_connections = '../data/ConnectiesHolland.csv'
max_trains = 7
max_time = 120

# create the stations from the file
stationsdict, connections = load(file_stations, file_connections)
stations = list(stationsdict.values())

quality, route = make_bad_routes(stations, max_trains, max_time, len(connections))

create_animation(stations, connections, route)