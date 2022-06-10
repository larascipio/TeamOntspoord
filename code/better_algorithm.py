from load import *
import argparse
import random

class Train():
    def __init__(self, route, starting_connection, max_time):
        """Creates a train at the starting point"""
        self._all_trains = route
        self._begin = starting_connection._stations[0]
        self._end = starting_connection._stations[1]
        self._route = [self._begin, self._end]
        self._connections = [starting_connection]
        # self._end_connection = None
        # self._begin_connection = None
        self._time = starting_connection._distance
        self._max_time = max_time
    
    def add_connection(self, connection):
        self._end = connection.get_destination(self._end)
        self._route.append(self._end)
        self._time += connection._distance
        self._connections.append(connection)

    def remove_last_connection(self):
        connection = self._connections.pop()
        self._route.pop()
        self._end = self._route[-1]
        self._time -= connection._distance
    
    def travel(self):
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
        if not indices[0] == len(qual) - 1:
            self.add_connection(self._end._connections[indices[0]])

class Routes():
    def __init__(self, stations, connections, max_trains, max_time):
        self._stations = {}
        self._connections = {}
        for station in stations:
            self._stations[station] = False
        for connection in connections:
            self._connections[connection] = False
        starting_connections = random.choices(connections, k=max_trains)
        self._trains = []
        stations = set()
        for connection in starting_connections:
            self._trains.append(Train(self, connection, max_time))
            self._connections[connection] = True
            self._stations[connection._stations[0]] = True
            self._stations[connection._stations[1]] = True
        # self._num_trains = max_trains
        self._num_connections = max_trains
        # self._tot_stations = len(stations)
        # self._tot_connections = len(connections)

    def num_trains(self) -> int:
        return len(self._trains)

    def num_stations(self) -> int:
        sum = 0
        for i in self._stations:
            if self._stations[i]:
                sum += 1
        return sum
    
    def num_connections(self) -> int:
        # sum = 0
        # for i in self._connections:
        #     if self._connections[i]:
        #         sum += 1
        # return sum
        cons = set()
        for train in self._trains:
            for con in train._connections:
                cons.add(con)
        return len(cons)

    def quality(self) -> float:
        qual = (self.num_connections()/len(self._connections))*10000
        for train in self._trains:
            qual -= 100
            qual -= train._time
        return qual
    
    def improve(self):
        for train in self._trains:
            # loop through connections to find the quality of each
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

    stations = list(load(file_stations, file_connections).values())
    route = Routes(stations, connectionlist, max_trains, max_time)
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
