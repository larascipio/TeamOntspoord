from load import *
import argparse
import random

class Train():
    def __init__(self, route, starting_connection, max_time):
        """
        Creates a route on the given connection.
        """
        
        # save the route that this train is a part of
        self._all_trains = route

        # initialize the starting route
        self._begin = starting_connection._stations[0]
        self._end = starting_connection._stations[1]
        self._route = [self._begin, self._end]
        self._connections = [starting_connection]

        # initialize the time and save the maximum allowed time
        self._time = starting_connection._distance
        self._max_time = max_time
    
    def add_connection(self, connection):
        """
        Adds the given connection to the end of the train, if it's connected to the last station.
        """
        
        # check if this connection is connected to the station
        if not self._end in connection._stations:
            return
        
        # add the connection
        self._end = connection.get_destination(self._end)
        self._route.append(self._end)
        self._time += connection._distance
        self._connections.append(connection)

    def remove_last_connection(self):
        """ 
        Removes the last connection of the route at the end of the train.
        Returns that connection.
        """
        
        # change the route and endpoint
        self._route.pop()
        self._end = self._route[-1]

        # remove and return the connection
        connection = self._connections.pop()
        self._time -= connection._distance
        return connection
    
    def travel(self):
        """
        Pick the best next connection to include in the route.
        If all connections lead to a worse score, don't change the route.
        """

        # figure out the quality for all possible connections
        qual = []
        for connection in self._end._connections:

            # add that connection
            self.add_connection(connection)

            # check and save the quality
            qual.append(self._all_trains.quality())

            # go back to the starting point
            self.remove_last_connection()

        # add the quality without chances
        qual.append(self._all_trains.quality())

        # find the best quality and use that connection
        indices = [index for index, item in enumerate(qual) if item == max(qual)]
        # print(qual, indices)

        # don't change anything if this already has the best score
        if indices[0] == len(qual) - 1:
            return
    
        self.add_connection(self._end._connections[indices[0]])


class Routes():
    def __init__(self, stations, connections, max_trains, max_time):
        """
        Create a route containing trains on the given railroad.
        """

        # choose random starting connections
        starting_connections = random.choices(connections, k=max_trains)
       
        # create the trains
        self._trains = []
        for connection in starting_connections:
            self._trains.append(Train(self, connection, max_time))
        
        # save the total amount of stations and connections in the railmap
        self._tot_stations = len(stations)
        self._tot_connections = len(connections)

    def num_trains(self) -> int:
        return len(self._trains)

    def num_stations(self) -> int: # TODO uiteindelijk kan deze hetzelfde als num_connections
        """
        Calculate the number of stations where trains have passed.
        """
        sum = 0
        for i in self._stations:
            if self._stations[i]:
                sum += 1
        return sum
    
    def num_connections(self) -> int:
        """
        Calculate the number of connections that have been passed.
        """
        cons = set()
        for train in self._trains:
            for con in train._connections:
                cons.add(con)
        return len(cons)

    def quality(self) -> float:
        """
        Calculate the quality of the current routes.
        """
        qual = (self.num_connections()/self._tot_connections)*10000
        for train in self._trains:
            qual -= 100
            qual -= train._time
        return qual
    
    def improve(self):
        """
        Change each train so the quality of the routes increases.
        """
        for train in self._trains:
            train.travel()

if __name__ == '__main__':

    # use commandline arguments to choose the railroad
    parser = argparse.ArgumentParser(description='create routes')
    parser.add_argument("type", choices=['holland','national'], help="Use the holland or national railroads")
    args = parser.parse_args()

    if args.type == 'holland':
        file_stations = '../data/StationsHolland.csv'
        file_connections = '../data/ConnectiesHolland.csv'
        max_trains = 7
        max_time = 120
    else:
        file_station = '../data/StationsNationaal.csv'
        file_connections = '../data/ConnectiesNationaal.csv'
        max_trains = 20
        max_time = 180

    # create the stations from the file
    stations = list(load(file_stations, file_connections).values())

    # create the route
    route = Routes(stations, connectionlist, max_trains, max_time)

    # keep improving the route, until it doesn't change
    old_qual = route.quality()
    print(route.quality())
    route.improve()
    new_qual = route.quality()
    while new_qual > old_qual:
        print(new_qual)
        route.improve()
        old_qual = new_qual
        new_qual = route.quality()
    print(route.quality())
