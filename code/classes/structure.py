from code.classes.stations import Station, Connection
import csv

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
        """Removes a failed stations from the dictionary, including all connections to it"""
        for connection in self._stations[failed_station]._connections:
            self.remove(connection)
            for station in connection._stations:
                if station is not stationdictionary[failed_station]:
                    station._connections.remove(connection)
                    if len(station._connections) == 0:
                        del stationdictionary[station]
        del self._stations[failed_station]

    def reset(self):

        # reset the stations
        for station in self._stations.values():
            station.reset()

        # reset the connections
        for connection in self._connections.values():
            connection.reset()