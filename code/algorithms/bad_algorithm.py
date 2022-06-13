import random

class Train():
    def __init__(self, starting_station, max_distance):
        """
        Create a train at the given station.
        """
        self._distance = 0
        self._current_station = starting_station
        self._route = [self._current_station._name] # TODO get name from station
        self._stations_traveled = [self._current_station]
        self._current_station.travel()
        self.running = True
        self._max_dist = max_distance

    def choose_connection(self):
        """
        Choose the first of the connections that has not been passed yet.
        """
        for connection in self._current_station._connections:
            if not connection.passed() and self._distance + connection._distance <= self._max_dist:
                return connection
        self.running = False
        return None

    def choose_random_connection(self):
        """
        Choose a random connection that has not been passed yet.
        """
        possible_connections = []
        weights = []
        for connection in self._current_station._connections:
            if not connection.passed() and self._distance + connection._distance <= self._max_dist:
                possible_connections.append(connection)
                if connection.get_destination(self._current_station).passed():
                    weights.append(1)
                else:
                    weights.append(2)
        if possible_connections:
            return random.choice(possible_connections)
        self.running = False
        return None
    
    def move(self, connection):
        """
        Move to a next station.
        """

        # increase the distance of the route
        self._distance += connection._distance # TODO

        # move the current station
        self._current_station = connection.get_destination(self._current_station)

        # set the connection and station to passed
        connection.travel()
        self._current_station.travel()

        # add the station to the route
        self._route.append(self._current_station._name)
        self._stations_traveled.append(self._current_station)
    
    def get_distance(self):
        return self._distance
    
    def get_route(self):
        return self._route


def make_bad_routes(stations: list, num_trains: int, max_distance: int, num_connections_not_passed: int):
    """
    Use the given railroads to create connections that satisfy the contraints.
    """
    end_stations = []
    for station in stations:
        if len(station._connections) % 2 == 1: # TODO nog veranderen in stations.py, misschien de hoeveelheid connecties in int opslaan?
            end_stations.append(station)
    print(end_stations)

    num_stations_not_passed = len(stations)
    # num_connections_not_passed = 89 # TODO dit moet nog uit load.py of stations.py komen

    trains = []
    # keep making trains until there are 8
    while len(trains) < num_trains and num_connections_not_passed > 0:
        
        # # check if all stations are passed
        # if num_stations_not_passed < 1:
        #     break
            
        # # check if all connections are passed
        # if num_connections_not_passed < 1:
        #     break

        start = None
        # choose starting point
        while not start:
            if len(end_stations) > 0:
            # choose one of the endstations
                start = end_stations.pop()
                
                # end = end_station.pop()
                # if not end.passed():
                #     start = end
            else:
                # choose a random station that has not been travelled
                for station in stations:
                    # print(station._name, station.passed())
                    # if not station.passed():
                    #     start = station
                    
                    # check if all connections are passed
                    for connection in station._connections:
                        if not connection.passed:
                            start = station
                            break
            

        # create the train with a distance of 0 and the starting station passed
        train = Train(start, max_distance)

        # keep going until the route is 2 hours
        while train.running:
            # connection = train.choose_connection()
            connection = train.choose_random_connection()
            if connection:
                if not connection.passed():
                    num_connections_not_passed -= 1
                train.move(connection)
                num_stations_not_passed -= 1
        
        if train._current_station in end_stations:
            end_stations.remove(train._current_station)
        trains.append(train)
        # print(num_stations_not_passed)
        # print(num_connections_not_passed)
        # print(train._route)
    
    # calculate the quality of this system of routes
    quality = (89 - num_connections_not_passed)/89 * 10000
    for train in trains:
        quality -= 100
        quality -= train.get_distance()
    
    # print(f"The quality of these routes is {quality}")

    return (quality, trains)

        
