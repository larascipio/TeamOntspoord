import random
from code.algorithms.random_algorithm import Make_Random_Routes
from code.classes.structure import Railnet
from code.classes.train import Train
import random
import copy 

class Depth_First():
    """
    A Depth First search algorithm.
    """

    def __init__(self, railnet):
        """
        Use network of routes to initialize the algorithm.
        """
        self._railnet = railnet
        #self._possible_stations = list(self._railnet.get_stations().values())
        self.get_random_routes()
        self._quality = self._railnet.quality()
        self._best_quality = self._quality

    def get_random_routes(self):
        """
        Use random algorithm to make a first train network .
        """
        route = Make_Random_Routes(self._railnet)
        route.run()

    def get_next_train(self):
        """
        Method that gets the next state from the list of states.
        """
        if len(self._copy_railnet_trains) > 0:
            return self._copy_railnet_trains.pop()
  
    
    def build_trains(self):
        """
        Creates all possible trajects from a single start station and returns them in a list.
        """
        # get start station
        #start_station = self._current_train._current_station
        route_current_train = self._current_train.get_stations()
        start_station = route_current_train[0]
        path = []
        list_of_trains = []
        stack = [start_station]
        print(f'Start {stack}')
        
        while stack:

            station = stack.pop()
            # new_train = self._copy_railnet.create_train(station)
            
            # if station not in path:
            #     path.append(station)
                
            for connection in station.get_connections():
                station = connection._stations[1]
                if not station._passed:
                    stack.append(station)
                    station._passed = True

            train = copy.deepcopy(stack)
            station_names = []
            for station in train:
                station_names.append(station._name)
            if len(station_names) > 0:
                list_of_trains.append(station_names)

            #print(list_of_trains)
        return list_of_trains

    def find_and_replace_best_train(self):
        """
        Checks and accepts better solutions than the current solution.
        """
        self._best_train = self._current_train
        for train in self._trains:
            # Add new train to the railnet 
            new_train = self._copy_railnet.restore_train(train)
            
            # Replace current train with better quality train
            if self.compare_quality():
                self._best_train = new_train

            self._copy_railnet.remove_train(new_train)

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
        # Keep initial quality of the railnet
        self._old_quality = self._quality

        # Copy the random train network to calculate net qualities
        self._copy_railnet = copy.deepcopy(self._railnet)
        print(f'Old {self._copy_railnet}')

        # Copy the random trains to use in get next train
        self._copy_railnet_trains = list(self._copy_railnet.get_trains())

        # Go through every train of random
        while self._copy_railnet_trains:

            # Take a train apart to search depth first 
            self._current_train = self.get_next_train()

            # Delete the train from copy railnet
            self._copy_railnet.remove_train(self._current_train)

            # Return all possible trains from same start station 
            self._trains = self.build_trains()
            print(f'TRAINS {self._trains}')

            # Find and replace by best train 
            # if self._trains: 
            self.find_and_replace_best_train()
            
            self._copy_railnet.add_train(self._best_train)

            print(f'New {self._copy_railnet}')


                
                



