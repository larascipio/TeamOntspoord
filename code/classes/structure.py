from all_code.classes.stations import Station, Connection
import csv
import random

class Railnet():
    def __init__(self):
        self._stations = {}
        self._connections = {}
        self._total_connections = 0

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
                self._total_connections += 1

    def get_stations(self):
        return self._stations

    def get_connections(self):
        return self._connections
    
    def get_total_connections(self) -> int:
        return self._total_connections

    def get_passed_connections(self) -> set:
        connections_passed = set()
        for connection in self._connections.values():
            if connection.passed():
                connections_passed.add(connection)
        return connections_passed

    def station_failure(self, failed_station):
        """Removes a failed station from the dictionary, including all connections to it"""
        if failed_station not in self._stations:
            return
        for unique_id in self._stations[failed_station]._connections:

            for station in self._connections[unique_id]._stations:

                # Remove the connection to the failed station in the station objects
                if station is not self._stations[failed_station]:
                    station.remove_connection(unique_id)
                    #if len(station._connections) == 0:
                        #del self._stations[station]

            # Remove the connection to the failed station from the dictionary
            del self._connections[unique_id]

        # Remove the failed station from the dictionary
        del self._stations[failed_station]

    def remove_random_connection(self):
        """Removes random connections"""
        uid = random.choice(list(self._connections.keys()))
        self.remove_connection(uid)

    def remove_connection(self, uid):
        """Removes connection"""
        for station in self._connections[uid]._stations:
                station.remove_connection(uid)
        del self._connections[uid]

    def add_connection(self, start, end):
        "Adds new connection"
        new_uid = max(self._connections) + 1

        # Create new distance from the coordinates
        if start._x > end._x:
            a = start._x - end._x
        else:
            a = end._x - start._x

        if start._y > end._y:
            b = start._y - end._y
        else:
            b = end._y - start._y

        c = a**2 + b**2
        distance = int(c**(1/2) * 100)

        connection = Connection(start, end, distance)
        start.add_connection(new_uid, connection)
        end.add_connection(new_uid, connection)
        self._connections[new_uid] = connection

    def change_connection(self):
        """Change connection from random start point to random end point"""

        # Get one of the stations from which connection will be changed
        start_connections = []
        start = random.choice(list(self._stations.values()))
        while len(start._connections) < 1:
            start = random.choice(list(self._stations.values()))

        # Get list of existing connecting stations
        for connection in start.get_connections():
            start_connections.append(connection.get_destination(start))

        # Get new end station
        end = random.choice(list(self._stations.values()))
        while end in start_connections:
            end = random.choice(list(self._stations.values()))

        # Remove an old connection and add the new connection
        removed_connection = random.choice(list(start._connections.keys()))
        self.remove_connection(removed_connection)
        self.add_connection(start, end)

    # def follow_track(self, route):
    #     """Follow all tracks again"""
    #     for track in route:
            
    #         # Makes sure the current stop is passed
    #         for i in range(len(track._route) - 1):
    #             current_stop = self._stations[track._route[i]]
    #             current_stop.travel()
    #             next_stop = self._stations[track._route[i + 1]]

    #             # Makes sure the connection is passed
    #             for connection in current_stop._connections:
    #                 if current_stop._connections[connection].get_destination(current_stop) == next_stop:
    #                     current_stop._connections[connection].travel()
    #                     break

    #         # Makes sure the final stop of the track is passed
    #         if len(track._route) > 1:
    #             next_stop.travel()
    
    def follow_track(self, route):
        for train in route:
            self.follow_train(train)

    def follow_train(self, train):
        # pass the stations
        for station in train.get_stations():
            station.travel()

        # pass the connections
        for connection in train.get_connections():
            connection.travel()

    def reset_track(self, route):
        for train in route:
            self.reset_train(train)

    def reset_train(self, train):

        # reset the stations
        for station in train.get_stations():
            station.reset()

        # reset the connections
        for connection in train.get_connections():
            connection.reset()

    def reset(self):

        # reset the stations
        for station in self._stations.values():
            station.reset()

        # reset the connections
        for connection in self._connections.values():
            connection.reset()