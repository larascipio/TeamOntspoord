import random

class Make_Bad_Routes():
    def __init__(self, railnet, num_trains: int, max_distance: int):
        """
        Create a network of routes.
        """
        self._railnet = railnet
        # self._stations = list(railnet.get_stations().values())
        # self._connections = list(railnet.get_connections())
        self._max_trains = num_trains
        self._max_dist = max_distance
        self._tot_stations = len(self._railnet.get_stations())
        self._tot_connections = len(self._railnet.get_connections())
        self._trains = []

        # find the endstations
        self._end_stations = []
        for station in self._railnet.get_stations().values():
            if len(station.get_connections()) % 2 == 1:
                self._end_stations.append(station)

    def run(self):
        while len(self._railnet.get_passed_connections()) < self._tot_connections:
            
            # check if there can be another train
            if len(self._trains) == self._max_trains:
                raise Exception('Too many trains made.')
            
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
            
            if train._current_station in self._end_stations:
                self._end_stations.remove(train._current_station)
            self._trains.append(train)
            # print(train)

    def create_train(self):
        start = None
        # choose starting point
        while not start:
            if len(self._end_stations) > 0:

            # choose one of the endstations
                start = self._end_stations.pop()
                
            else:
                # choose a random station that has not been travelled
                for station in self._railnet.get_stations():
                    # check if all connections are passed
                    if set(station.get_connections()) - self._route.get_passed_connections():
                        start = station
                        break
                
                # there are no stations left for new trains.
                raise Exception('Cannot create a new train.')

        return Train(self, start, self._max_dist)


    def get_trains(self):
        return self._trains

    # def all_connections_passed(self) -> set:
    #     connections = set()

    #     # for train in self._trains:
    #     #     connections = connections | set(train.get_connections())

    #     for connection in self._route.get_connections.values():
    #         if connection.passed():
    #             connections.add(connection)
        
    #     return connections
            

    def all_stations_passed(self) -> set:
        """
        Give a set of all stations passed.
        """
        stations = set()
        for train in self._route.get_trains.values():
            stations.add(train.get_stations())
        return stations

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
        # self._current_station.travel()
        self._running = True
        self._max_dist = max_distance
    
    def is_running(self):
        return self._running

    def stop(self):
        self._running = False

    def get_connections(self):
        return self._connections_traveled

    def get_stations(self):
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

    def choose_random_connection(self):
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


    def move(self, connection):
        """
        Move to a next station.
        """
        # print(self._current_station)
        # increase the distance of the route
        self._distance += connection.get_distance()

        # move the current station
        self._current_station = connection.get_destination(self._current_station)

        # add the station and connection to the route
        self._route.append(self._current_station.get_name())
        self._stations_traveled.append(self._current_station)
        self._connections_traveled.append(connection)
        connection.travel()
        # print(self.get_connections())
        # print(self._distance)
        # print()
    
    def get_distance(self):
        return self._distance
    
    def get_route(self):
        return self._route

    def __repr__(self):
        return f'Train: {[station for station in self._stations_traveled]}'


def make_bad_routes(stations: list, connections: list, num_trains: int, max_distance: int):
    """
    Use the given railroads to create connections that satisfy the contraints.
    """
    # end_stations = []
    # for station in stations:
    #     if len(station.get_connections()) % 2 == 1:
    #         end_stations.append(station)
    # # print(end_stations)

    route = Make_Bad_Routes(stations, connections, num_trains, max_distance)
    route.run()


    # num_stations_not_passed = len(stations)
    # num_connections_not_passed = 89 # TODO dit moet nog uit load.py of stations.py komen

    # trains = []
    # # keep making trains until there are 8
    # while len(trains) < num_trains and num_connections_not_passed > 0:
        
    #     # # check if all stations are passed
    #     # if num_stations_not_passed < 1:
    #     #     break
            
    #     # # check if all connections are passed
    #     # if num_connections_not_passed < 1:
    #     #     break

    #     start = None
    #     # choose starting point
    #     while not start:
    #         if len(end_stations) > 0:
    #         # choose one of the endstations
    #             start = end_stations.pop()
                
    #             # end = end_station.pop()
    #             # if not end.passed():
    #             #     start = end
    #         else:
    #             # choose a random station that has not been travelled
    #             for station in stations:
    #                 # print(station._name, station.passed())
    #                 # if not station.passed():
    #                 #     start = station
                    
    #                 # check if all connections are passed
    #                 for connection in station._connections:
    #                     if not connection.passed:
    #                         start = station
    #                         break
            

    #     # create the train with a distance of 0 and the starting station passed
    #     train = Train(start, max_distance)

    #     # keep going until the route is 2 hours
    #     while train.running:
    #         # connection = train.choose_connection()
    #         connection = train.choose_random_connection()
    #         if connection:
    #             if not connection.passed():
    #                 num_connections_not_passed -= 1
    #             train.move(connection)
    #             num_stations_not_passed -= 1
        
    #     if train._current_station in end_stations:
    #         end_stations.remove(train._current_station)
    #     trains.append(train)
    #     # print(num_stations_not_passed)
    #     # print(num_connections_not_passed)
    #     # print(train._route)
    
    # # calculate the quality of this system of routes
    # quality = (89 - num_connections_not_passed)/89 * 10000
    # for train in trains:
    #     quality -= 100
    #     quality -= train.get_distance()
    
    # # print(f"The quality of these routes is {quality}")



        
