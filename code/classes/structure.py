"""
structure.py

Programmeertheorie - minor programmeren
Lara, Tim, Eva

- Houses the main structure for the algorithms to use; Railnet.
- Railnet contains trains (train.py), stations and connections (station.py).
"""

# ------------------------------- Imports --------------------------------------

from code.classes.stations_and_connections import Station, Connection
from code.classes.train import Train
# import plotly.express as px
import csv
import random

# ------------------------------- Railnet --------------------------------------


class Railnet():
    def __init__(self, num_trains: int, max_distance: int):
        """Create a railnet with files given."""
        self._stations = {}
        self._connections = []
        self._trains = []
        self._max_trains = num_trains
        self._max_dist = max_distance

        # create the colors for the trains
        self._colorset = {
            'fuchsia', 'red', 'cyan', 'blue', 'darkorange', 'green',
            'darkviolet', 'black', 'gold', 'deeppink', 'lime', 'darkred'
        }

    def load(self, file_locations: str, file_connections: str):
        """
        Load the stations and its connections from the provided files.
        """

        with open(file_locations, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                new_station = Station(row['station'], row['x'], row['y'])
                self._stations[row['station']] = new_station

        with open(file_connections, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                connection = Connection(
                    self._stations[row['station1']],
                    self._stations[row['station2']],
                    float(row['distance'])
                )
                self._connections.append(connection)
                self._stations[row['station1']].add_connection(connection)
                self._stations[row['station2']].add_connection(connection)

    def get_stations(self) -> dict:
        return self._stations

    def get_connections(self) -> list:
        return self._connections

    def get_trains(self) -> list:
        return self._trains

    def get_total_connections(self) -> int:
        return len(self._connections)
    
    def get_total_stations(self) -> int:
        return len(self._stations)

    def get_passed_connections(self) -> set:
        connections_passed = set()
        for connection in self._connections:
            if connection.passed():
                connections_passed.add(connection)
        return connections_passed

    def get_max_trains(self) -> int:
        return self._max_trains

    def get_max_distance(self) -> int:
        return self._max_dist

    def all_colors_used(self) -> set:
        """
        Return a set with all colors used by the trains in the railnet.
        Used by self.create_train to determine the color for a next train.
        """
        colors = set()
        for train in self._trains:
            colors.add(train.get_color())
        return colors

    def __repr__(self):
        representation = 'Route:\n'
        for train in self._trains:
            representation += f'{train}' + '\n'
        representation += f'quality = {self.quality()}'
        return representation

    # --------------------------- Trains ---------------------------------------

    def create_train(self, start):
        """
        Create a train at the given station.
        """
        available_colors = self._colorset - self.all_colors_used()
        if available_colors:
            color = random.sample(available_colors, 1)[0]
        else:
            color = random.sample(self._colorset, 1)[0]

        train = Train(self, start, color)

        self._trains.append(train)

        return train

    def remove_train(self, train):
        """
        Remove the given train from the railnet.
        """
        if train not in self._trains:
            raise Exception('This train does not exist.')

        for connection in train.get_connections():
            connection.remove()

        self._trains.remove(train)

    # --------------------------- Quality --------------------------------------

    def quality(self) -> float:
        """
        Calculate the quality of the current routes.
        """
        # calculate points for the ratio of connections passed
        qual = (len(self.get_passed_connections())
                / self.get_total_connections())*10000

        # remove 100 points and the distance traveled per train
        for train in self._trains:
            qual -= 100
            qual -= train.get_distance()

        return qual

    def get_max_quality(self) -> float:
        """
        Get the theoretical maximum quality for the railroad.
        """

        # calculate the total distance of all connections
        total_distance = 0
        for connection in self.get_connections():
            total_distance += connection.get_distance()

        # calculate the minimum amount of trains needed for the total distance
        minimum_trains = (total_distance // self._max_dist + 1)

        # calculate the quality with these variables
        theoretical_quality = 10000 - minimum_trains*100 - total_distance

        return theoretical_quality

    # --------------------------- Changing the railnet -------------------------

    def station_failure(self, failed_station) -> list:
        """
        Remove all connections to and from a failed station.
        Return a list of removed connections for possible restoration.
        """
        if failed_station not in self._stations:
            raise Exception('This station does not exist.')

        # make a list of removed stations for restoration
        removed_station_list = []

        # copy the removed connections, so they can be restored later
        failed_connections = self._stations[failed_station].get_connections().copy()

        # remove the connections, save removed stations in the list
        for connection in failed_connections:

            removed_stations = self.remove_connection(connection)
            removed_station_list.extend(removed_stations)

        # return list of connections and stations for possible restoration
        return failed_connections, removed_station_list

    def remove_connection(self, connection) -> list:
        """
        Remove connection.
        Remove stations without connections.
        """
        removed_station_list = []

        for station in connection.get_stations():

            station.remove_connection(connection)

            # if a station has no more connections
            if len(station.get_connections()) == 0:

                # delete the station and save it for restoration
                removed_station_list.append(station)
                del self._stations[station.get_name()]

        self._connections.remove(connection)

        return removed_station_list

    def restore_connection(self, connection):
        """
        Restore connection that was removed.
        """
        for station in connection.get_stations():
            if connection not in station.get_connections():
                station.add_connection(connection)

        self._connections.append(connection)

    def restore_station(self, station):
        """
        Restore station that was removed
        """
        self._stations[station.get_name()] = station

    def add_connection(self, start, end):
        """
        Add new connection with start and end point.
        Return connection.
        """

        # calculate new distance from the coordinates
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
        start.add_connection(connection)
        end.add_connection(connection)
        self._connections.append(connection)

        return connection

    def change_connection(self):
        """
        Change connection from random start point to random end point.
        Only where the connection did not exist before.
        Return the removed and added connection.
        """

        # get one of the stations from which connection will be changed
        start_connections = []
        start = random.choice(list(self._stations.values()))
        while len(start.get_connections()) < 1:
            start = random.choice(list(self._stations.values()))

        # get list of existing connecting stations
        for connection in start.get_connections():
            start_connections.append(connection.get_destination(start))

        # get new end station
        end = random.choice(list(self._stations.values()))
        while end in start_connections:
            end = random.choice(list(self._stations.values()))

        # remove an old connection and add the new connection
        removed_connection = random.choice(start.get_connections())
        removed_station_list = self.remove_connection(removed_connection)
        added_connection = self.add_connection(start, end)

        return removed_connection, added_connection, removed_station_list

    # --------------------------- Changing routes ------------------------------

    def reset(self):
        """
        Completely reset the railnet.
        Used for a loop where algorithms are run multiple times.
        """
        # reset the stations
        for station in self._stations.values():
            station.reset()

        # reset the connections
        for connection in self._connections:
            connection.reset()

        self._trains = []

    def add_route(self, route):
        """
        Add an existing list of trains to the railnet.
        """
        self._trains = route
        self.follow_track()

    def add_train(self, train):
        """
        Add existing train to the railnet.
        Used by random_iteration.py and biased_iteration.py
        """
        self.follow_train(train)
        self._trains.append(train)

    def follow_track(self):
        """
        Pass all connections and stations.
        Used by restore_routes().
        """
        for train in self._trains:
            self.follow_train(train)

    def follow_train(self, train):
        """
        Pass all connections and stations of a given train.
        """
        # pass the stations
        for station in train.get_stations():
            station.travel()

        # pass the connections
        for connection in train.get_connections():
            connection.travel()

    # --------------------------- Changing routes without trains ---------------

    def get_route_names(self) -> list:
        """
        Return a list of lists with names of all stations passed.
        Used by Reheating (simulated_annealing.py).
        """
        route = []

        # loop through all trains to create the route
        for train in self._trains:

            # create a list with all stationnames
            stations = []
            for station in train.get_stations():
                stations.append(station.get_name())

            # add this list to the total route
            route.append(stations)
        return route

    def restore_routes(self, route_names: list):
        """
        Restore the given route if the railnet was reset.
        The given list contains lists with the names of the stations.
        Used by Reheating (simulated_annealing.py).
        """
        if self._trains != []:
            raise Exception('This railnet was not yet reset.')

        # restore each train
        for train in route_names:
            self.restore_train(train)

    def restore_train(self, train_stations: list):
        """
        Restore the given route.
        The given list contains the names of the stations.
        Used by restore_routes.
        """

        # check if the list has names
        if not train_stations:
            raise Exception('This is an empty list')

        # create new train
        train_copy = train_stations.copy()
        new_train = self.create_train(self._stations[train_stations[0]])

        # move the train over the stations
        for next_station in train_stations:
            station = new_train.get_stations()[-1]
            connection = station.get_connection_by_station(next_station)
            if connection:
                new_train.move(connection)
            else:
                raise Exception('This combination of station is not possible.')

        return new_train
