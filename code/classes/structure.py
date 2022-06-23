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
        colorlist = px.colors.qualitative.Vivid[:-1]
        self._color = colorlist + colorlist + colorlist

    def load(self, file_locations: str, file_connections: str):
        """Load the stations and its connections"""
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
        train = Train(self, start, self._color.pop())
        self._trains.append(train)
        return train

    def remove_train(self, train):
        """
        Remove the given train from the railnet.
        """
        # if train in self._trains:
        #     self._trains.remove(train)
        #     self.reset_train(train)
        if not train in self._trains:
            raise Exception('This train does not exist.')

        for connection in train.get_connections():
            connection.remove()
        
        self._trains.remove(train)

    def add_train(self, train):
        """
        Add existing train to the railnet
        """
        self.follow_train(train)
        self._trains.append(train)

    def remove_last_train(self):
        train = self._trains.pop()
        self.reset_train(train)
        return train

    def remove_first_train(self):
        train = self._trains.pop(0)
        self.reset_train(train)
        return train

    def add_route(self, route):
        self._trains = route
        self.follow_track()

    def get_stations(self):
        return self._stations

    def get_connections(self):
        return self._connections

    def get_trains(self):
        return self._trains
    
    def get_total_connections(self) -> int:
        return len(self._connections)

    def get_passed_connections(self) -> set:
        connections_passed = set()
        for connection in self._connections:
            if connection.passed():
                connections_passed.add(connection)
        return connections_passed

    def get_max_trains(self):
        return self._max_trains

    def get_max_distance(self):
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

    def reset_track(self):
        for train in self._trains:
            self.reset_train(train)

    def reset_train(self, train):

        # reset the stations
        # for station in train.get_stations():
        #     station.remove()

        # reset the connections
        for connection in train.get_connections():
            connection.reset()

    def reset(self):

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
        The higher the quality difference, the more negatively the train affects the quality
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

    def station_failure(self, failed_station):
        """Removes a failed station from the dictionary, including all connections to it"""
        if failed_station not in self._stations:
            # TODO moet hier niet een error komen?
            return

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
        """Removes random connections"""
        connection = random.choice(self._connections)
        self.remove_connection(connection)

    def remove_connection(self, connection):
        """Removes connection"""
        for station in connection.get_stations():
                station.remove_connection(connection)
        self._connections.remove(connection)
        # self._total_connections -= 1

    def add_connection(self, start, end):
        "Adds new connection"

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
        start.add_connection(connection)
        end.add_connection(connection)
        self._connections.append(connection)
        # self._total_connections += 1

    def change_connection(self):
        """Change connection from random start point to random end point"""

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
    
    def follow_track(self):
        for train in self._trains:
            self.follow_train(train)

    def follow_train(self, train):
        # pass the stations
        for station in train.get_stations():
            station.travel()

        # pass the connections
        for connection in train.get_connections():
            connection.travel()



    def __repr__(self):
        representation = 'Route:\n'
        for train in self._trains:
            representation += f'{train}' + '\n'
        representation += f'quality = {self.quality()}'
        return representation
