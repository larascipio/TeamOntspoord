from stations import *
import csv

stationdictionary = {}

with open("../data/StationsHolland.csv", newline = '') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader: 
        new_station = Station(row['station'], row['x'], row['y'])
        stationdictionary[row['station']] = new_station

print(stationdictionary)


with open("../data/ConnectiesHolland.csv", newline = '') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader: 
        connection = Connection(row['station1'], row['station2'], row['distance'])
        stationdictionary[row['station1']].add_connection(connection)
        stationdictionary[row['station2']].add_connection(connection)

for station in stationdictionary:
    print(stationdictionary[station]._connections)

