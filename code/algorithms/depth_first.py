"""
depth_first.py

Programmeertheorie - minor programmeren
Lara, Tim, Eva

- This algorithm improves a random train network by using depth first search. 
- Uses the Railnet structure.
- Uses the random algorithm to create starting routes.
"""
from code.algorithms.random_algorithm import Make_Random_Routes
import copy 

class Depth_First():
    def __init__(self, railnet):
        """
        Create a random train network.
        """
        self._railnet = railnet
        self.get_random_routes()

    def get_random_routes(self):
        """
        Use random algorithm to make a first train network.
        """
        route = Make_Random_Routes(self._railnet)
        route.run()

    def get_next_train(self):
        """
        Method that returns the first train station of traject.
        """
        if len(self._copy_railnet_trains) > 0:
            return self._copy_railnet_trains.pop(0)
  
    def find_best_train(self):
        """
        Create all possible trains from a given start station and returns best train.
        """
        best_quality = 0 
        best_train = None
        start_station = self._current_train.get_station_names()[0]
        
        # first station is the first parent node
        stack = [[start_station]]
        
        # find all child nodes to create possible trains
        while stack:
            # take the last added station names
            stations = stack.pop()
            # create a train from station names
            train = self._railnet.restore_train(stations)

            quality = self._railnet.quality()
            # check if this train is the best train 
            if quality >= best_quality:
                best_quality = quality
                best_train = stations
            
            # get last station to find possible connections
            last_station = train.get_stations()[-1]
            
            # add every connecting station to the current station in the stack
            connections = last_station.get_connections()
            for connection in connections: 
                # check if train is not too long 
                if connection.get_distance() + train.get_distance() <= self._railnet.get_max_distance():
                    station = connection.get_destination(last_station)
                    stations.append(station.get_name())
                    stack.append(stations.copy())
                    stations.pop()

            # remove current train to add new train again 
            self._railnet.remove_train(train)

        return best_train 
        
    def run(self):
        """
        Run the algorithm.
        """
        self._copy_railnet_trains = list(self._railnet.get_trains())

        # go through every train of the railnet
        for _ in range(len(self._copy_railnet_trains)):

            # take a train apart to search for better train 
            self._current_train = self.get_next_train()

            # delete old train  
            self._railnet.remove_train(self._current_train)

            # find the best train
            self._best_train = self.find_best_train()

            # add new better train 
            self._railnet.restore_train(self._best_train) 


