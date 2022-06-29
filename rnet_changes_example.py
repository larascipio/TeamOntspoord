"""
rnet_changes_example.py

Programmeertheorie - minor programmeren
Lara, Tim, Eva

- Can be used to test functions that change the railnet
- Example on how to change the structure of the railnet
"""

# ------------------------------- Imports --------------------------------------

from code.classes.structure import Railnet
import random

file_stations = 'data/StationsNationaal.csv'
file_connections = 'data/ConnectiesNationaal.csv'
max_trains = 20
max_time = 180

# ------------------------------- Testing --------------------------------------

# loads the railnet
rails = Railnet(max_trains, max_time)
rails.load(file_stations, file_connections)

# get the theoretical optimum
first_max = rails.get_max_quality()

# get a random failed_station
failed_station = random.choice(list(rails.get_stations().keys()))

# remove connections to a failed station, then restore them
connectionlist, removed_station_list = rails.station_failure(failed_station)

# if the quality hasn't changed, the functions don't work!
if first_max == rails.get_max_quality():
    print('failure!')

for removed_station in removed_station_list:
    rails.restore_station(removed_station)
for connection in connectionlist:
    rails.restore_connection(connection)

# change random connection, then restore to its former state
old_connection, new_connection, removed_station_list = rails.change_connection()

# if the quality hasn't changed, the functions don't work!
if first_max == rails.get_max_quality():
    print('failure!')

for removed_station in removed_station_list:
    rails.restore_station(removed_station)
rails.restore_connection(old_connection)
rails.remove_connection(new_connection)

final_max = rails.get_max_quality()

# if the quality hasn't changed, the functions work!
if first_max == final_max:
    print('success!')
