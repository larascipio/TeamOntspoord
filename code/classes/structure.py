"""
structure.py

Programmeertheorie - minor programmeren
Lara, Tim, Eva

- Houses the main structure for the algorithms to use; Railnet.
- Railnet contains trains (train.py), stations and connections (station.py).
"""

# ------------------------------- Imports --------------------------------------

from code.classes.stations import Station, Connection
from code.classes.train import Train
# import plotly.express as px
import csv
import random

# ------------------------------- Railnet --------------------------------------

class Railnet(): # TODO misschien is het logischer als de load ook in de init wordt aangeroepen
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

        with open(file_locations, newline = '') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader: 
                new_station = Station(row['station'], row['x'], row['y'])
                self._stations[row['station']] = new_station

        with open(file_connections, newline = '') as csvfile:
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
                # uid += 1
                # self._total_connections += 1

    def get_stations(self) -> dict:
        return self._stations

    def get_connections(self) -> list:
        return self._connections

    def get_trains(self) -> list:
        return self._trains
    
    def get_total_connections(self) -> int:
        return len(self._connections)

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
        Returns a set with all colors used by the trains in the railnet.
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

    # --------------------------- trains ---------------------------------------

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
        if not train in self._trains:
            raise Exception('This train does not exist.')

        for connection in train.get_connections():
            connection.remove()

        self._trains.remove(train)

    # def remove_train_connections(self, train): # TODO where is this used? kan t niet gwn in de code
    #     """
    #     Remove the effect train had on connections.
    #     """
    #     for connection in train.get_connections():
    #         connection.remove()

    # --------------------------- Quality --------------------------------------

    def quality(self) -> float:
        """
        Calculate the quality of the current routes.
        """
        # calculate points for the ratio of connections passed
        qual = (len(self.get_passed_connections())
            /self.get_total_connections())*10000
        
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
        Removes all connections to and from a failed station.
        Return a list of removed connections for possible restoration.
        """
        if failed_station not in self._stations:
            raise Exception('This station does not exist.')

        failed_connections = self._stations[failed_station].get_connections().copy() # TODO < waarom maak je hier een copy?

        for connection in failed_connections:

            self.remove_connection(connection)

        # Remove the failed station from the dictionary
        # del self._stations[failed_station]
        return failed_connections

    def remove_random_connection(self):
        """
        Removes random connection.
        Returns connection for possible restoration.
        """
        connection = random.choice(self._connections)
        self.remove_connection(connection)

        return connection

    def remove_connection(self, connection):
        """
        Removes connection.
        """
        for station in connection.get_stations():

            station.remove_connection(connection)
            #if len(station.get_connections()) == 0:
                #del self._stations[station]

        self._connections.remove(connection)

    def restore_multiple_connections(self, connectionlist: list): # TODO waar wordt dit gebruikt?
        """
        Restore multiple connections. TODO waarom niet loopen waar het gebruikt wordt?
        """
        for connection in connectionlist:
            self.restore_connection(connection)

    def restore_connection(self, connection):
        """
        Restore connection that was removed.
        """
        for station in connection.get_stations():
            if connection not in station.get_connections():
                station.add_connection(connection)

        self._connections.append(connection)

    def add_connection(self, start, end):
        """
        Adds new connection with start and end point.
        Returns connection.
        """

        # Calculate new distance from the coordinates
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
        Returns the removed and added connection.
        """

        # Get one of the stations from which connection will be changed
        start_connections = []
        start = random.choice(list(self._stations.values()))
        while len(start.get_connections()) < 1:
            start = random.choice(list(self._stations.values()))

        # Get list of existing connecting stations
        for connection in start.get_connections():
            start_connections.append(connection.get_destination(start))

        # Get new end station
        end = random.choice(list(self._stations.values()))
        while end in start_connections:
            end = random.choice(list(self._stations.values()))

        # Remove an old connection and add the new connection
        removed_connection = random.choice(start.get_connections())
        self.remove_connection(removed_connection)
        added_connection = self.add_connection(start, end)

        return removed_connection, added_connection

    def empty_railnet(self): # TODO where is this used?
        """
        Empty the railnet, so new stations 
        and connections can be loaded in.
        """
        self._stations = {}
        self._connections = []
    
    # --------------------------- Changing routes ------------------------------

    def reset(self):
        """
        Completely resets the railnet.
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
        Passes all connections and stations.
        Used by restore_routes().
        """
        for train in self._trains:
            self.follow_train(train)

    def follow_train(self, train):
        """
        Passes all connections and stations of a given train.
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
        Returns a list of lists with names of all stations passed.
        Used by Reheating (simulated_annealing.py).
        """
        route = []
        for train in self._trains:
            route.append(train.get_station_names())
        return route

    def restore_routes(self, route_names: list):
        """
        Restores the given route if the railnet was reset.
        The give list contains lists with the names of the stations.
        Used by Reheating (simulated_annealing.py).
        """
        if self._trains != []:
            raise Exception('This railnet was not yet reset.')
        
        for train in route_names:

            # create new train
            new_train = self.create_train(self._stations[train.pop(0)])

            # move the train over the stations
            while train:
                station = new_train.get_stations()[-1]
                connection = station.get_connection_by_station(train.pop(0))
                new_train.move(connection)

    # --------------------------- Archived methods -----------------------------

    # def remove_last_train(self):
    #     """
    #     Removes and returns last train from the railnet.
    #     Used by random_iteration.py and biased_iteration.py
    #     """
    #     train = self._trains.pop()
    #     self.remove_train_connections(train)

    #     return train

    # def remove_first_train(self):
    #     """
    #     Removes and returns first train from the railnet.
    #     Used by random_iteration.py and biased_iteration.py
    #     """
    #     train = self._trains.pop(0)
    #     self.remove_train_connections(train)

    #     return train

    
    # def run_random_train(self, train):
    #     """
    #     Choose a random connection for the train to use.
    #     Used by random_algorithm.py
    #     """
    #     while train.is_running():

    #         connection = train.choose_random_connection()
    #         if not connection:
    #             break
    #         self.move_train(train, connection)

    # def run_biased_train(self, train):
    #     """
    #     Choose an unused connection for the train to use.
    #     Used by biased_iteration.py
    #     """
    #     while train.is_running():

    #         connection = train.choose_next_connection()
    #         if not connection:
    #             break
    #         self.move_train(train, connection)

    # def move_train(self, train, connection):
    #     """
    #     Move the train to a new station if possible.
    #     """
    #     if connection.get_distance() + train.get_distance() < self._max_dist:
    #         train.move(connection)
    #     else:
    #         train.stop()


    # def check_trains_quality(self):
    #     """
    #     Check how each train affects the quality. 
    #     Store in two lists so duplicate scores aren't overwritten.
    #     The higher the quality difference, the more negatively the 
    #     train affects the quality.
    #     """
    #     self.overall_quality = self.quality()
    #     iterated_train_list = []
    #     quality_list = []

    #     for train in self._trains:
    #         self.remove_train(train)

    #         quality_difference = self.quality() - self.overall_quality
    #         iterated_train_list.append(train)
    #         quality_list.append(quality_difference)

    #         self.add_train(train)

    #     return iterated_train_list, quality_list
