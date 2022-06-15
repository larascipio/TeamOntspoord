import random

class Make_Random_Routes():
    def __init__(self, railnet, num_trains: int, max_distance: int):
        """
        Create a train at the given station.
        """
        self._railnet = railnet
        self._max_trains = num_trains
        self._max_dist = max_distance
        self._tot_stations = len(self._railnet.get_stations())
        self._tot_connections = len(self._railnet.get_connections())
        self._trains = []
    
    def run(self):
        """
        Run the algorithm.
        """
        amount_of_trains = 0
        # check whether not all connections have been passed 
        while len(self._railnet.get_passed_connections()) < self._tot_connections:
    
            
            for _ in range(self._max_trains):
                # create a train
                train = self.create_train()
                if not train:
                    return

            # keep going until the route is 2 hours
            while train.is_running():
                # connection = train.choose_connection()
                connection = train.choose_random_connection()

                if not connection:
                    break

                if connection.get_distance() + train.get_distance() < self._max_dist:
                    train.move(connection)
                else:
                    train.stop()

            # save the train
            self._trains.append(train)
    
    def create_train(self):
        """
        Create a new train at a random start station.
        """
        start = None
        # choose random starting point
        while not start:
            # choose a random start station 
            possible_stations = []
            for station in self._railnet.get_stations().values():
                possible_stations.append(station)
            start = random.choice(possible_stations)

        return Train(self, start, self._max_dist)
    
    def get_trains(self):
        return self._trains
    
    def choose_random_connection(self):
        """
        Choose a random connection.
        """
        possible_connections = []
        for connection in self._current_station.get_connections():
                possible_connections.append(connection)
        if possible_connections:
            return random.choice(list(possible_connections))

        # no more possible connections
        self.stop()
        return None
    
    def quality(self) -> float:
        """
        Calculate the quality of the current routes.
        """
        qual = (len(self._railnet.get_passed_connections())/self._tot_connections)*10000
        for train in self._trains:
            qual -= 100
            qual -= train.get_distance()
        return qual

    def __repr__(self):
        representation = 'Route:\n'
        for train in self._trains:
            representation += f'{train}' + '\n'
        representation += f'quality = {self.quality()}'
        return representation
    
    
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

    def choose_random_connection(self):
            """
            Choose a random connection.
            """
            
            possible_connections = []
            for connection in self._current_station.get_connections():
                possible_connections.append(connection)
            if possible_connections:
                return random.choice(list(possible_connections))

            # no more possible connections
            self.stop()
            return None

    def move(self, connection):
        """
        Move to a next station.
        """

    # increase the distance of the route
        self._distance += connection.get_distance()

        # move the current station
        self._current_station = connection.get_destination(self._current_station)

        # add the station and connection to the route
        self._route.append(self._current_station.get_name())
        self._stations_traveled.append(self._current_station)
        self._connections_traveled.append(connection)
        connection.travel()
    
    def get_distance(self):
        return self._distance
    
    def get_route(self):
        return self._route

    def __repr__(self):
        return f'Train: {[station for station in self._stations_traveled]}'


# def Make_Random_Routes(stations: list, connections: list, max_trains:int, max_distance: int):
#     """
#     Use the given railroads to create connections that satisfy the contraints.
#     """
#     # Choose a random starting point 
#     start = random.choice(stations)
        
#     # Create a train with a random start station, and a max dist
#     train = Train(start, connections, max_distance)

#     # keep going until the route is 2 hours
#     while train.running:
#         connection = train.choose_random_connection()
#         if connection:
#             if not connection.passed():
#                 num_connections_not_passed -= 1
#             train.move(connection)
#             num_stations_not_passed -= 1
    
#     if train._current_station in end_stations:
#         end_stations.remove(train._current_station)
#     trains.append(train)


# # calculate the quality of this system of routes
#     quality = (89 - num_connections_not_passed)/89 * 10000
#     for train in trains:
#         quality -= 100
#         quality -= train.get_distance()

#     # print(f"The quality of these routes is {quality}")

#     return (quality, trains)

        
