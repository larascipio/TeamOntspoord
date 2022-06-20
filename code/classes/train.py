import random

class Train():
    def __init__(self, routes, starting_station, max_distance):
        """
        Create a train at the given station.
        """
        self._routes = routes
        self._distance = 0
        self._current_station = starting_station
        self._route = [self._current_station.get_name()]
        self._stations_traveled = [self._current_station]
        self._connections_traveled = []
        # self._current_station.travel()
        self._running = True
        self._max_dist = max_distance
    
    def is_running(self):
        """ Check if this train is still running. """
        return self._running

    def stop(self):
        """ Stop the train. """
        self._running = False

    def get_connections(self):
        """ Get all the connections that this train has in its route. """
        return self._connections_traveled

    def get_stations(self):
        """ Get all the stations in this trains route. """
        return self._stations_traveled

    # def choose_connection(self):
    #     """
    #     Choose the first of the connections that has not been passed yet.
    #     """
    #     print(self._current_station, self._current_station.get_connections() - self._routes.all_connections_passed())
    #     for connection in self._current_station.get_connections() - self._routes.all_connections_passed():
    #         if self._distance + connection.get_distance() <= self._max_dist:
    #             return connection
    #     self._running = False
    #     return None

    def choose_next_connection(self):
        """
        Choose a random connection that has not been passed yet.
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


        
        # this train cannot go further

    def choose_random_connection(self):
        """
        Choose a random connection.
        """

        weights = [self._distance/self._max_dist]
        counter = 0
        possible_connections = ["stop"]
        for connection in self._current_station.get_connections():
                counter += 1
                possible_connections.append(connection)
                weights.append(1)
        # print(weights)

        choice = random.choices(possible_connections, weights, k=1)
        if choice[0] == "stop":
            self.is_running = False
            return None
        return choice[0]

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
        self._route.append(next_station.get_name())
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
        self._route.pop()

    def movestart(self, connection):
        """
        Move to a next station from the end of the train.
        """
        self._distance += connection.get_distance()

        new_station = connection.get_destination(self._stations_traveled[0])

        self._route.insert(0, new_station.get_name())
        self._stations_traveled.insert(0, new_station)
        self._connections_traveled.insert(0, connection)
        connection.travel()
    
    def remove_first_connection(self):
        first_connection = self._connections_traveled.pop(0)
        self._distance -= first_connection.get_distance()
        first_connection.remove()
        
        self._stations_traveled.pop(0)
        self._route.pop(0)
    
    def get_distance(self):
        return self._distance
    
    def get_route(self):
        return self._route

    def __repr__(self):
        return f'Train: {[station for station in self._stations_traveled]}'
