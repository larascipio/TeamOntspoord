"""
main.py
"""
from code.classes.load import load, print_stationdictionary
from code.algorithms.random_algorithm import make_random_routes
from code.visualisation.plotly_animation import create_animation

import argparse

if __name__ == '__main__':

    # use commandline arguments to choose the railroad
    parser = argparse.ArgumentParser(description='create routes')
    parser.add_argument("type", choices=['holland','national'], help="Use the holland or national railroads")
    args = parser.parse_args()

    if args.type == 'holland':
        file_stations = 'data/StationsHolland.csv'
        file_connections = 'data/ConnectiesHolland.csv'
        max_trains = 7
        max_time = 120
    else:
        file_stations = 'data/StationsNationaal.csv'
        file_connections = 'data/ConnectiesNationaal.csv'
        max_trains = 20
        max_time = 180

    
    qualityroutes = {}
    stationdict, connectionlist = load(file_stations, file_connections)
    print(connectionlist)

    for _ in range(1):
        route = make_random_routes(list(stationdict.values()), connectionlist, max_trains, max_time)
        route.run()
        quality = route.quality()

        print(route)

        # create_animation(list(stationdict.values()), connectionlist, route)
    

        # quality, route = make_bad_routes(list(stationdictionary.values()), connectionlist, 7, 120)

        # qualityroutes[quality] = route
        # for connection in connectionlist:
        #     print(connection._passed)
    
    # # Create hist for best routes 
    # quality_hist(qualityroutes)


    # """
# random algoritm (klad bestand)
# """

# import random

# def get_available_connections(stations):
#     available_connections = []
#     for station in stations:
#         for connection in stations[station]._connections:
#             if connection._passed is False:
#                 available_connections.append(connection)
#     return available_connections

# def random_route(connections):
#      # Select a connection
#     connection = random.choice(connections)
    
#     # First station passed 
#     connection._stations[1]._passed = True
#     connection._passed = True 
    
#     distance_route = 0
#     route = [connection._stations[1]]

#     while distance_route <= 120:
#         possible_connections = get_available_connections(connections)
#         for connection in connection._stations[1]._connections:
#             if connection._passed is False:
#                 possible_connections.append(connection)
    
#         connection = random.choice(possible_connections) 
#         connection._stations[1]._passed = True
#         connection._passed = True
#         route.append(connection._stations[1])
#         distance_route += connection._distance
#     print(route)
#     return route 

# def passed_connections(connections):
#     pass

# def passed_station(self):
#     pass

# if __name__ == '__main__':
#     file_stations = './data/StationsNationaal.csv'
#     file_connections = './data/ConnectiesNationaal.csv'

#     stations = load(file_stations, file_connections)

#     # Get all non-passed connections
#     available_connections = get_available_connections(stations)
    
#     # Start route with a random connection
#     route = random_route(available_connections)

#     # Check if all connections are passed 
#     passed_connections

        # get connection with shortest distance
        # shortest = 63
        # for connection in start_station[1]._connections:
        #     if connection._distance < shortest:
        #         shortest  = connection._distance
        #         shortest_connection = connection
        # choose random connection
    	
        # connection = random.choice(station[1]._connections)
        # if connection._passed == False:
        #     connection._passed = True
        # else:
        #     connection = random.choice(station[1]._connections)
        # station = connection._stations[1]
        
        # distance_route += connection._distance
        # print(distance_route)
    
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

        
