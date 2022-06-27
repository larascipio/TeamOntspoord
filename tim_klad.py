from code.classes.structure import Railnet
import random

file_stations = 'data/StationsNationaal.csv'
file_connections = 'data/ConnectiesNationaal.csv'
max_trains = 20
max_time = 180

# Loads the railnet
rails = Railnet(max_trains, max_time)
rails.load(file_stations, file_connections)

first_max = rails.get_max_quality()

# Get a random failed_station
failed_station = random.choice(list(rails.get_stations().keys()))

# Remove connections to a failed station, then restore them
connectionlist, removed_station_list = rails.station_failure(failed_station)

# If the quality hasn't changed, the functions don't work!
if first_max == rails.get_max_quality():
    print('failure!')

for removed_station in removed_station_list:
    rails.restore_station(removed_station)
for connection in connectionlist:
    rails.restore_connection(connection)

# Change random connection, then restore to its former state
old_connection, new_connection, removed_station_list = rails.change_connection()

# If the quality hasn't changed, the functions don't work!
if first_max == rails.get_max_quality():
    print('failure!')

for removed_station in removed_station_list:
    rails.restore_station(removed_station)
rails.restore_connection(old_connection)
rails.remove_connection(new_connection)

# Remove random connection, then restore it.
removed_connection = rails.remove_random_connection()

# If the quality hasn't changed, the functions don't work!
if first_max == rails.get_max_quality():
    print('failure!')
    
rails.restore_connection(removed_connection)

final_max = rails.get_max_quality()

# If the quality hasn't changed, the functions work!
if first_max == final_max:
    print('success!')

# Check the quality for each station, if it were removed
# stationlist = list(rails.get_stations().values())
# minus_distance = 0
# quality_difference_dict = {}


# for station in stationlist:
#     for connection in station.get_connections():
#         minus_distance += connection.get_distance()

#     total_distance = 1551 - minus_distance
#     minus_trains = (total_distance // max_time + 1) * 100
#     theoretical_quality = 10000 - minus_trains - total_distance
#     quality_difference_dict[station.get_name()] = theoretical_quality
#     minus_distance = 0

# print(quality_difference_dict)

    
#     rails.reset
#     rails.load(file_stations, file_connections)



