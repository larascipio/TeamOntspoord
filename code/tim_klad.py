from load import *
import matplotlib.pyplot as plt
import random

stationdictionary = {}
connectionlist = []

def load(file_locations: str, file_connections: str):
    """Load the stations and its connections"""


    with open(file_locations, newline = '') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader: 
            new_station = Station(row['station'], row['x'], row['y'])
            stationdictionary[row['station']] = new_station

    with open(file_connections, newline = '') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader: 
            connection = Connection(stationdictionary[row['station1']], stationdictionary[row['station2']], row['distance'])
            connectionlist.append(connection)
            stationdictionary[row['station1']].add_connection(connection)
            stationdictionary[row['station2']].add_connection(connection)

    return stationdictionary

def visualize_tracks():
    """Visualizes all the tracks in a plot"""
    plt.figure(figsize=(12, 25))

    for station in list(stationdictionary.values()):
        plt.plot(float(station._x), float(station._y), 'o')
        plt.annotate(station._name, (float(station._x), float(station._y)))

    for connection in connectionlist:
        begin = [float(connection._stations[0]._x), float(connection._stations[1]._x)]
        end = [float(connection._stations[0]._y), float(connection._stations[1]._y)]
        plt.plot(begin, end, color='g')

    plt.title('Stations')
    plt.savefig('new_station.png')

# TODO, check connections, ipv stations. Stations opslaan zodat je niet terug gaat naar beginstation

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


def make_bad_routes():
    end_stations = []
    weighted_chance = []
    other_end_stations = []
    # TODO Start-station weighted chance - miss ook weighted chance for de andere
    for station in list(stationdictionary.values()):
        if len(station._connections) < 2: # TODO nog veranderen in stations.py, misschien de hoeveelheid connecties in int opslaan?
            end_stations.append(station)
        else:
            weighted_chance.append(len(station._connections))
            other_end_stations.append(station._name)

    
    for station in list(stationdictionary.values()):
        weighted_chance.append(len(station._connections))

    weighted_chance_start = [1 / x for x in weighted_chance]

    
    num_stations_not_passed = len(list(stationdictionary.values()))
    num_connections_not_passed = len(connectionlist)

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
            for station in list(stationdictionary.values()):
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
    
    quality = (len(connectionlist) - num_connections_not_passed)/len(connectionlist) * 10000
    for train in trains:
        quality -= 1
        quality -= train.get_distance()
    
    # print(f"The quality of these routes is {quality}")

    return (quality, trains)

if __name__ == "__main__":
    file_stations = '../data/StationsHolland.csv'
    file_connections = '../data/ConnectiesHolland.csv'
    load(file_stations, file_connections)
    visualize_tracks()



