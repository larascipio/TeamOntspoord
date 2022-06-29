from multiprocessing import connection
from opcode import stack_effect
from code.algorithms.random_algorithm import Make_Random_Routes
from code.algorithms.bad_algorithm import Make_Greedy_Routes
import copy 
from code.visualisation.plotly_animation import create_animation

class Depth_First():
    """
    A Depth First search algorithm.
    """

    def __init__(self, railnet):
        """
        Use network of routes to initialize the algorithm.
        """
        self._railnet = railnet
        self.get_random_routes()
        self._quality = self._railnet.quality()
        self._best_quality = self._quality

    def get_random_routes(self):
        """
        Use random algorithm to make a first train network.
        """
        route = Make_Random_Routes(self._railnet)
        # route = Make_Greedy_Routes(self._railnet)
        route.run()

    def get_next_train(self):
        """
        Method that returns the first train station of traject.
        """
        if len(self._copy_railnet_trains) > 0:
            return self._copy_railnet_trains.pop(0)
  
    def build_trains(self):
        """
        Creates all possible trajects from a single start station and returns them in a list of stations.
        """

        best_quality = 0 
        best_train = None
        start_station = self._current_train.get_station_names()[0]
        # aangepast naar current train
        stack = [[start_station]]
        
        while stack:
            # take the last added station names
            stations = stack.pop()
            # create a train from station names
            train = self._copy_railnet.restore_train(stations)
            quality = self._copy_railnet.quality()
            # check if this train is the best train 
            if quality >= best_quality:
                best_quality = quality
                best_train = stations
            
            last_station = train.get_stations()[-1]
            
            connections = last_station.get_connections()
            for connection in connections: 
                if connection.get_distance() + train.get_distance() <= self._copy_railnet.get_max_distance():
                    station = connection.get_destination(last_station)
                    stations.append(station.get_name())
                    stack.append(stations.copy())
                    stations.pop()

            self._copy_railnet.remove_train(train)

            
        return best_train 

    def find_and_replace_best_train(self, possible_trains):
        """
        Checks and accepts better solutions than the current solution.
        """
        # print(possible_trains)
        # TODO waarom geef je possible trains mee?
        self._possible_trains = possible_trains

        best_train = self._current_train
        for train in self._possible_trains:
            # Add new train to the railnet 
            new_train = self._copy_railnet.restore_train(train)
            #print(self._copy_railnet)
            # Replace current train with better quality train
            if self.compare_quality():
                best_train = new_train

            self._copy_railnet.remove_train(new_train)
        return best_train

    def compare_quality(self):
        """
        Checks and accepts better solutions than the current solution.
        """
        new_quality = self._copy_railnet.quality()
        
        if new_quality >= self._old_quality:
            self._best_quality = new_quality
            return True
        
    def run(self):
        """
        Run the algorithm.
        """

        #create_animation(self._railnet)

        # save initial quality of the train network
        self._old_quality = self._quality

        # Copy train network to delete and change trains
        self._copy_railnet = copy.deepcopy(self._railnet)
        # print(f'Old {self._copy_railnet}')

        self._copy_railnet_trains = list(self._copy_railnet.get_trains())
        # print(f'copy_railnet_trains: {self._copy_railnet_trains}')

        # Go through every train of the railnet
        for _ in range(len(self._copy_railnet_trains)):
            # Take a train apart to search depth first 
            self._current_train = self.get_next_train()

            # Delete the train from train network 
            self._copy_railnet.remove_train(self._current_train)

            # TODO name function
            best_train = self.build_trains()

            self._copy_railnet.restore_train(best_train)

            print(f'New {self._copy_railnet}')



