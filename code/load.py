from stations import *
import csv

stationdictionary = {}

with open("../data/StationsHolland.csv", newline = '') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader: 
        new_station = Station(row['station'], row['x'], row['y'])
        stationdictionary[row['station']] = new_station

with open("../data/ConnectiesHolland.csv", newline = '') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader: 
        connection = Connection(stationdictionary[row['station1']], stationdictionary[row['station2']], row['distance'])
        stationdictionary[row['station1']].add_connection(connection)
        stationdictionary[row['station2']].add_connection(connection)

for station in stationdictionary:
    stationdictionary[station].print_info()

