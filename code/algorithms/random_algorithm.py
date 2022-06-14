import random

class Train():
    def __init__(self, starting_station, connections, max_distance):
        """
        Create a train at the given station.
        """
        self._distance = 0
        self._current_station = starting_station
        self._total_connections = connections
        self._route = [self._current_station._name] 
        self._stations_traveled = [self._current_station]
        # self._current_station.travel()
        self.running = True
        self._max_dist = max_distance

    def choose_random_connection(self):
        """
        Choose a random connection.
        """
        possible_connections = []
        for connection in self._current_station._connections:
            if self._distance + connection._distance <= self._max_dist:
                possible_connections.append(connection)
        if possible_connections:
            random_connection =  random.choice(possible_connections)
            self._total_connections.remove(random_connection)
        self.running = False
        return None
    
    # def move(self, connection):
    #     """
    #     Move to a next station.
    #     """

    #     # increase the distance of the route
    #     self._distance += connection._distance # TODO

    #     # move the current station
    #     self._current_station = connection.get_destination(self._current_station)

    #     # set the connection and station to passed
    #     connection.travel()
    #     self._current_station.travel()

    #     # add the station to the route
    #     self._route.append(self._current_station._name)
    #     self._stations_traveled.append(self._current_station)
    
    # def get_distance(self):
    #     return self._distance
    
    # def get_route(self):
    #     return self._route


def make_random_routes(stations: list, connections: list, max_trains:int, max_distance: int):
    """
    Use the given railroads to create connections that satisfy the contraints.
    """
    # Choose a random starting point 
    start = random.choice(stations)
        
    # Create a train with a random start station, and a max dist
    train = Train(start, connections, max_distance)

    # keep going until the route is 2 hours
    while train.running:
        connection = train.choose_random_connection()
        if connection:
            if not connection.passed():
                num_connections_not_passed -= 1
            train.move(connection)
            num_stations_not_passed -= 1
    
    if train._current_station in end_stations:
        end_stations.remove(train._current_station)
    trains.append(train)


# calculate the quality of this system of routes
    quality = (89 - num_connections_not_passed)/89 * 10000
    for train in trains:
        quality -= 100
        quality -= train.get_distance()

    # print(f"The quality of these routes is {quality}")

    return (quality, trains)

        
