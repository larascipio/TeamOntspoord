from code.classes.stations import Station, Connection
import csv
import random

class Railnet():
    def __init__(self):
        self._stations = {}
        self._connections = {}

    def load(self, file_locations: str, file_connections: str):
        """Load the stations and its connections"""
        with open(file_locations, newline = '') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader: 
                new_station = Station(row['station'], row['x'], row['y'])
                self._stations[row['station']] = new_station

        with open(file_connections, newline = '') as csvfile:
            reader = csv.DictReader(csvfile)
            uid = 0
            for row in reader: 
                connection = Connection(self._stations[row['station1']], self._stations[row['station2']], float(row['distance']))
                self._connections[uid] = connection
                self._stations[row['station1']].add_connection(uid, connection)
                self._stations[row['station2']].add_connection(uid, connection)
                uid += 1

    def get_stations(self):
        return self._stations

    def get_connections(self):
        return self._connections

    def get_passed_connections(self) -> set:
        connections_passed = set()
        for connection in self._connections.values():
            if connection.passed():
                connections_passed.add(connection)
        return connections_passed

    def station_failure(self, failed_station):
        """Removes a failed station from the dictionary, including all connections to it"""
        for unique_id in self._stations[failed_station]._connections:

            for station in self._connections[unique_id]:

                # Remove the connection to the failed station in the station objects
                if station is not self._stations[failed_station]:
                    station.remove_connection(unique_id)
                    #if len(station._connections) == 0:
                        #del self._stations[station]

            # Remove the connection to the failed station from the dictionary
            del self._connections[unique_id]

        # Remove the failed station from the dictionary
        del self._stations[failed_station]

    def remove_random_connections(self):
        """Removes three random connections"""
        for i in range(3):
            removed_connection = random.choice(list(self._connections.values()))
            self.remove_connection(removed_connection)

    def remove_connection(self, removed_connection):
        """Removes connection"""
        for station in removed_connection._stations:
                station.remove_connection(removed_connection)
        del self._connections[removed_connection]

    def add_connection(self, start, end):
        "Adds new connection"
        new_uid = max(self._connections) + 1
        # TODO pas distance aan
        distance = 20
        connection = Connection(start, end, distance)
        start.add_connection(new_uid, connection)
        end.add_connection(new_uid, connection)
        self._connections[new_uid] = connection

    def change_connection(self):
        """Change connection from random start point to random end point"""

        # Get one of the stations from which connection will be changed
        start_connections = []
        start = random.choice(list(self._stations.values()))

        # Get list of existing connecting stations
        for connection in start.get_connections():
            start_connections.append(connection.get_destination(start))

        # Get new end station
        end = random.choice(list(self._stations.values()))
        while end in start_connections:
            end = random.choice(list(self._stations.values()))

        # Remove an old connection and add the new connection
        removed_connection = random.choice(start._connections)
        self.remove_connection(removed_connection)
        self.add_connection(start, end)

    def follow_track(self, route):
        """Follow all tracks again"""
        for track in route:
            
            # Makes sure the current stop is passed
            for i in range(len(track._route) - 1):
                current_stop = self._stations[track._route[i]]
                current_stop.travel()
                next_stop = self._stations[track._route[i + 1]]

                # Makes sure the connection is passed
                for connection in current_stop._connections:
                    if connection.get_destination(current_stop) == next_stop:
                        connection.travel()
                        break

            # Makes sure the final stop of the track is passed
            next_stop.travel()

    def reset(self):

        # reset the stations
        for station in self._stations.values():
            station.reset()

        # reset the connections
        for connection in self._connections.values():
            connection.reset()