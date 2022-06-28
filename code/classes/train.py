"""
train.py

Programmeertheorie - minor programmeren
Lara, Tim, Eva

- Contains the Train class.
"""

# --------------------------------- Imports ------------------------------------

import random

# --------------------------------- Train --------------------------------------

class Train():
    def __init__(self, routes, starting_station, color):
        """
        Create a train at the given station.
        """
        self._routes = routes
        self._distance = 0
        self._current_station = starting_station
        self._station_names = [self._current_station.get_name()]
        self._stations_traveled = [self._current_station]
        self._connections_traveled = []
        # self._current_station.travel()
        self._running = True
        self._color = color
    
    def is_running(self) -> bool:
        """ Check if this train is still running. """
        return self._running

    def stop(self) -> None:
        """ Stop the train. """
        self._running = False

    def get_connections(self) -> list:
        """ Get all the connections that this train has in its route. """
        return self._connections_traveled

    def get_stations(self) -> list:
        """ Get all the stations in this trains route. """
        return self._stations_traveled
    
    def get_color(self) -> tuple:
        return self._color

    def get_distance(self):
        return self._distance
    
    def get_station_names(self):
        return self._station_names

    def __repr__(self):
        return f'Train: {[station for station in self._stations_traveled]}'

    # --------------------------- Different choosing methods -------------------
    
    def choose_next_connection(self):
        """
        Choose a random connection that has not been passed yet.
        Used by the greedy algorithm.
        """
        possible_connections = []
        for connection in self._current_station.get_connections():
            if not connection.passed():
                possible_connections.append(connection)
        if possible_connections:
            return random.choice(list(possible_connections))

        # no more possible connections
        self.stop()
        return None

        # possible_connections = []
        # weights = []
        # for connection in self._current_station.get_connections():
        #     if connection not in self._routes.all_connections_passed() and self._distance + connection.get_distance() <= self._max_dist:
                
        #         # this connections is possible
        #         possible_connections.append(connection)
        #         if connection.get_destination(self._current_station) in self._routes.all_connections_passed():
        #             weights.append(1)
        #         else:
        #             weights.append(2)

    def choose_shortest_connection(self):
        """
        Choose the shortest connection that has not been passed yet.
        """
        distance = 100
        for connection in self._current_station.get_connections():
            if not connection.passed():
                if connection._distance < distance:
                    distance = connection._distance 
                    chosen_connection = connection
                return chosen_connection

        # no more possible connections
        self.stop()
        return None

    def choose_longest_connection(self):
        """
        Choose if possible the inbetween connection that has not been passed yet.
        """
        distance = 0
        for connection in self._current_station.get_connections():
            if not connection.passed():
                if connection._distance > distance:
                    distance = connection._distance 
                    chosen_connection = connection
                return chosen_connection

        # no more possible connections
        self.stop()
        return None

    def weighted_connection(self):
        possible_connections = []
        for connection in self._current_station.get_connections():
            if not connection.passed():
                possible_connections.append(connection)
        if possible_connections:
            return random.choice(list(possible_connections))

        # no more possible connections
        self.stop()
        return None

    def choose_random_connection(self):
        """
        Choose a random connection.
        """

        weights = [self._distance/self._routes.get_max_distance()]
        counter = 0
        possible_connections = ["stop"]
        for connection in self._current_station.get_connections():
                counter += 1
                possible_connections.append(connection)
                weights.append(1)

        choice = random.choices(possible_connections, weights, k=1)
        if choice[0] == "stop":
            self.is_running = False
            return None
        return choice[0]

    def choose_first_connection(self):
        """
        Choose the next connection if the list of possible connections
        that has not been passed yet.
        """
        possible_connections = []
        for connection in self._current_station.get_connections():
            if not connection.passed():
                possible_connections.append(connection)
        if possible_connections:
            return possible_connections[0]

        # no more possible connections
        self.stop()
        return None

    def get_possible_connections(self):
        possible_connections = []
        for connection in self._current_station.get_connections():
            if not connection.passed():
                possible_connections.append(connection)
        if possible_connections:
            return possible_connections

    # --------------------------- Changing the train ---------------------------

    def move(self, connection):
        """
        Move to a next station from the front of the train.
        """
        # print(self._current_station)

        # increase the distance of the route
        self._distance += connection.get_distance()

        # move the current station
        next_station = connection.get_destination(self._stations_traveled[-1])
        self._current_station = next_station

        # add the station and connection to the route
        self._station_names.append(next_station.get_name())
        self._stations_traveled.append(next_station)
        self._connections_traveled.append(connection)
        connection.travel()
        # print(self.get_connections())
        # print(self._distance)
        # print()

    def remove_last_connection(self):
        last_connection = self._connections_traveled.pop()
        self._distance -= last_connection.get_distance()
        last_connection.remove()

        self._stations_traveled.pop()
        self._current_station = self._stations_traveled[-1]
        self._station_names.pop()

    def movestart(self, connection):
        """
        Move to a next station from the end of the train.
        """
        self._distance += connection.get_distance()

        new_station = connection.get_destination(self._stations_traveled[0])

        self._station_names.insert(0, new_station.get_name())
        self._stations_traveled.insert(0, new_station)
        self._connections_traveled.insert(0, connection)
        connection.travel()
    
    def remove_first_connection(self):
        first_connection = self._connections_traveled.pop(0)
        self._distance -= first_connection.get_distance()
        first_connection.remove()
        
        self._stations_traveled.pop(0)
        self._station_names.pop(0)
        return first_connection
