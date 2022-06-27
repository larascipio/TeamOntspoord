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
        self._possible_stations = list(self._railnet.get_stations().values())
        self.get_random_routes()
        # print(self._railnet)
        self._best_route = None
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
        return self._railnet._trains.pop()
    
    def build_trains(self):
        """
        Creates all possible child-connections from one train and adds them to the list of states.
        """
        # all possible trains from a start station
        possible_trains = []
        
        # get start station
        start_station = self._current_train._current_station

        # create train 
        train = self._railnet.create_train(start_station)
        
        while train.choose_first_connection() != None:
            connection = train.choose_first_connection()
            train.move(connection)
            
        possible_trains.append(train)
        print(possible_trains)
        return train 

    def find_best_train():
        pass

    def check_solution(self):
        """
        Checks and accepts better solutions than the current solution.
        """
        if self._new_quality >= self._old_quality:
            self._best_quality = self._new_quality
    
    def run(self):
        """
        Run the algorithm.
        """
        # Copy the random trains
        self._stack = copy.deepcopy(list(self._railnet.get_trains()))
        self._old_quality = self._quality
        print(f'Old {self._railnet}')
        
        # Go through every route of random and change it with depth first 
        while len(self._stack) != 0:

            # Remove train from stack to change connections
            self._current_train = self.get_next_train()
            if self._current_train is not None:
                
                # Build and find trains with highest quality 
                train = self.build_trains()
                
                # Add train to current route
                #self._railnet.add_train(train)
                print(f'New {self._railnet}')

                # Calculate quality with different train
                self._new_quality = self._railnet.quality()
                
            
    