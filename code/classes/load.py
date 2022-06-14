from code.classes.stations import Station, Connection
import csv


def load(file_locations: str, file_connections: str):
    """Load the stations and its connections"""
    stationdictionary = {}
    connectionlist = []

    with open(file_locations, newline = '') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader: 
            new_station = Station(row['station'], row['x'], row['y'])
            stationdictionary[row['station']] = new_station

    with open(file_connections, newline = '') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader: 
            connection = Connection(stationdictionary[row['station1']], stationdictionary[row['station2']], float(row['distance']))
            connectionlist.append(connection)
            stationdictionary[row['station1']].add_connection(connection)
            stationdictionary[row['station2']].add_connection(connection)

    return (stationdictionary, connectionlist)

def reset():
    pass

def print_stationdictionary(stationdictionary):
    """Prints out all the information form the dictionary"""
    for station in stationdictionary:
        stationdictionary[station].print_info()

