from code.classes.stations import Station, Connection
from code.classes.train import Train
import plotly.express as px
import csv
import random

class Railnet():
    def __init__(self, num_trains: int, max_distance: int):
        self._stations = {}
        self._connections = []
        self._trains = []
        self._max_trains = num_trains
        self._max_dist = max_distance

        # create the colors for the trains
        # self._colorlist = px.colors.qualitative.Vivid[:-1] + px.colors.qualitative.Dark2[:-1]
        self._colorset = {'fuchsia', 'red', 'cyan', 'blue', 'darkorange', 'green', 'darkviolet', 'black', 'gold', 'deeppink', 'lime', 'darkred'}
        # self._color = self._colorlist.copy()

    def load(self, file_locations: str, file_connections: str):
        """
        Load the stations and its connections.
        """

        with open(file_locations, newline = '') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader: 
                new_station = Station(row['station'], row['x'], row['y'])
                self._stations[row['station']] = new_station

        with open(file_connections, newline = '') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader: 
                connection = Connection(self._stations[row['station1']], self._stations[row['station2']], float(row['distance']))
                self._connections.append(connection)
                self._stations[row['station1']].add_connection(connection)
                self._stations[row['station2']].add_connection(connection)
                # uid += 1
                # self._total_connections += 1

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

        # if len(self._color) < len(self._colorlist):
        #     self._color += self._colorlist.copy()
        # train = Train(self, start, self._color.pop())
        self._trains.append(train)

        return train

    def remove_train(self, train):
        """
        Remove the given train from the railnet.
        """
        if not train in self._trains:
            raise Exception('This train does not exist.')

        self.remove_train_connections(train)
        self._trains.remove(train)

    def add_train(self, train):
        """
        Add existing train to the railnet.
        """
        self.follow_train(train)
        self._trains.append(train)

    def remove_last_train(self):
        """
        Removes and returns last train from the railnet.
        """
        train = self._trains.pop()
        self.remove_train_connections(train)

        return train

    def remove_first_train(self):
        """
        Removes and returns first train from the railnet.
        """
        train = self._trains.pop(0)
        self.remove_train_connections(train)

        return train

    def remove_train_connections(self, train):
        """
        Remove effect train had on connections.
        """
        for connection in train.get_connections():
            connection.remove()

    def add_route(self, route):
        """
        Add set of trains to the railnet.
        """
        self._trains = route
        self.follow_track()

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

    def quality(self) -> float:
        """
        Calculate the quality of the current routes.
        """
        qual = (len(self.get_passed_connections())/self.get_total_connections())*10000
        
        for train in self._trains:
            qual -= 100
            qual -= train.get_distance()
        
        return qual

    def reset(self):
        """
        Completely resets the railnet.
        """
        # reset the stations
        for station in self._stations.values():
            station.reset()

        # reset the connections
        for connection in self._connections:
            connection.reset()

        self._trains = []

    def check_trains_quality(self):
        """
        Check how each train affects the quality. 
        Store in two lists so duplicate scores aren't overwritten.
        The higher the quality difference, the more negatively the 
        train affects the quality.
        """
        self.overall_quality = self.quality()
        iterated_train_list = []
        quality_list = []

        for train in self._trains:
            self.remove_train(train)

            quality_difference = self.quality() - self.overall_quality
            iterated_train_list.append(train)
            quality_list.append(quality_difference)

            self.add_train(train)

        return iterated_train_list, quality_list

    def get_max_quality(self) -> float:
        """
        Get the theoretical maximum quality for the railroad.
        """
        total_distance = 0

        for connection in self.get_connections():
            total_distance += connection.get_distance()

        minus_trains = (total_distance // self._max_dist + 1) * 100
        theoretical_quality = 10000 - minus_trains - total_distance

        return theoretical_quality

    def station_failure(self, failed_station):
        """
        Removes all connections to and from a failed station.
        """
        if failed_station not in self._stations:
            raise Exception('This station does not exist.')

        for connection in self._stations[failed_station].get_connections():

            for station in connection.get_stations():

                station.remove_connection(connection)
                #if len(station._connections) == 0:
                    #del self._stations[station]

            # Remove the connection to the failed station from the dictionary
            self._connections.remove(connection)

        # Remove the failed station from the dictionary
        # del self._stations[failed_station]

    def remove_random_connection(self):
        """
        Removes random connection.
        """
        connection = random.choice(self._connections)
        self.remove_connection(connection)

    def remove_connection(self, connection):
        """
        Removes connection.
        """
        for station in connection.get_stations():
                station.remove_connection(connection)
        self._connections.remove(connection)

    def add_connection(self, start, end):
        """
        Adds new connection with start and end point.
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

    def change_connection(self):
        """
        Change connection from random start point to random end point.
        Only where the connection did not exist before.
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
        self.add_connection(start, end)

    def empty_railnet(self):
        """
        Empty the railnet, so new stations 
        and connections can be loaded in.
        """
        self._stations = {}
        self._connections = []
    
    def follow_track(self):
        """
        Passes all connections and stations.
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

    def all_colors_used(self) -> set:
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
