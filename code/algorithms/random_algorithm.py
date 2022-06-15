import random
import numpy as np

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
        # Create a random max distance (BIAS: not higher than input max distance)
        # self._random_distance = random.randint(1, self._max_dist)

        # Create a random amount of trains within the constraint (BIAS: 0 = eruit )
        self._random_amount = random.randint(1, self._max_trains)
        for _ in range(self._random_amount):
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
        
        stop_weight = 0.1
        weights = [stop_weight]
        counter = 0
        possible_connections = ["stop"]
        for connection in self._current_station.get_connections():
                counter += 1
                possible_connections.append(connection)
        connection_weight = (1 - stop_weight) / counter
        for _ in range(counter):
            weights.append(connection_weight)
        print(weights)
        if possible_connections:
            choice = np.random.choice(possible_connections, 1, p=weights)
            if choice[0] == "stop":
                self.is_running = False 
                return None
            return choice[0] 

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

        
