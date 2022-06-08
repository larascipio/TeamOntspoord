import random

class Train():
    def __init__(self, starting_station):
        self._distance = 0
        self._current_station = starting_station
        self._route = [self._current_station._name] # TODO get name from station
        self._current_station.travel()
        self.running = True

    def choose_connection(self):
        for connection in self._current_station._connections:
            if not connection.passed() and self._distance + connection._distance <= 120:
                return connection
        self.running = False
        return None

    def choose_random_connection(self):
        possible_connections = []
        weights = []
        for connection in self._current_station._connections:
            if not connection.passed() and self._distance + connection._distance <= 120:
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

        # increase the distance of the route
        self._distance += connection._distance # TODO

        # move the current station
        self._current_station = connection.get_destination(self._current_station)

        # set the connection and station to passed
        connection.travel()
        self._current_station.travel()

        # add the station to the route
        self._route.append(self._current_station._name)
    
    def get_distance(self):
        return self._distance
    
    def get_route(self):
        return self._route


def make_bad_routes(stations: list):
    end_stations = []
    for station in stations:
        if len(station._connections) < 2: # TODO nog veranderen in stations.py, misschien de hoeveelheid connecties in int opslaan?
            end_stations.append(station)
    
    num_stations_not_passed = len(stations)
    num_connections_not_passed = 28 # TODO dit moet nog uit load.py of stations.py komen

    trains = []
    # keep making trains until there are 8
    while len(trains) < 8:
        
        # check if all stations are passed
        if num_stations_not_passed < 1:
            break

        # choose starting point
        if len(end_stations) > 0:
            # choose one of the endstations
            start = end_stations.pop()
        else:
            # choose a random station that has not been travelled
            for station in stations:
                # print(station._name, station.passed())
                if not station.passed():
                    start = station
                    break
            

        # create the train with a distance of 0 and the starting station passed
        train = Train(start)

        # keep going until the route is 2 hours
        while train.running:
            # connection = train.choose_connection()
            connection = train.choose_random_connection()
            if connection:
                if not connection.passed():
                    num_connections_not_passed -= 1
                train.move(connection)
                num_stations_not_passed -= 1
        
        trains.append(train)
        # print(num_stations_not_passed)
        # print(num_connections_not_passed)
        # print(train._route)
    
    quality = (28 - num_connections_not_passed)/28 * 10000
    for train in trains:
        quality -= 1
        quality -= train.get_distance()
    
    # print(f"The quality of these routes is {quality}")

    return (quality, trains)

        
