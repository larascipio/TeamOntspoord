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
        if len(self._copy_railnet_trains) > 0:
            return self._copy_railnet_trains.pop()
  
    
    def build_trains(self):
        """
        Creates all possible trajects from a single start station and returns them in a list.
        """
        # all possible trains from a start station
        
    
        # get start station
        #start_station = self._current_train._current_station
        route_current_train = self._current_train.get_stations()
        start_station = route_current_train[0]
        path = []
        list_of_trains = []
        stack = [start_station]
        #print(f'Start {stack}')
        
        while stack:

            station = stack.pop()

            if station not in path:
                path.append(station)
            # else:
            #     continue
                
                for connection in station.get_connections():
                    station = connection._stations[1]
                    if not station._passed:
                        stack.append(station)
                        station._passed = True 
                
                #print(f'Stack {stack}')
                train = copy.deepcopy(stack)
                train = Train()
                list_of_trains.append(train)
                
        return list_of_trains

    def find_best_train(self):
        """
        Checks and accepts better solutions than the current solution.
        """
        for train in self._trains:
            print("1")
            print(self._copy_railnet)
            print("2")
            print(self._current_train)
            changed_train = self._copy_railnet._trains.pop()
            self._copy_railnet.add_train(train)
            print(self._copy_railnet)
            self._new_quality = self._copy_railnet.quality()
            if self._new_quality >= self._old_quality:
                self._best_quality = self._new_quality 

    # def check_solution(self, train):
    #     """
    #     Checks and accepts better solutions than the current solution.
    #     """
    #     if self._new_quality >= self._old_quality:
    #         self._best_quality = self._new_quality
    
    def run(self):
        """
        Run the algorithm.
        """
        # Copy the random train network 
        self._copy_railnet = copy.deepcopy(self._railnet)
        # Copy the random train
        self._copy_railnet_trains = copy.deepcopy(list(self._railnet.get_trains()))
        #self._copy_railnet_trains = list(self._copy_railnet.get_trains())
       # print(self._copy_railnet)
        self._old_quality = self._quality
        print(f'Old {self._railnet}')

        # Go through every route of random and change it with depth first 
        while self._copy_railnet_trains:

            # Remove train from stack to change connections
            self._current_train = self.get_next_train()
            if self._current_train is not None:
                
                # Build and find trains with highest quality 
                self._trains = self.build_trains()

                if self._trains: 
                    self.find_best_train()
                
                # Add train to current route
                self._railnet.add_train(train)
                print(f'New {self._railnet}')

                # Calculate quality with different train
                self._new_quality = self._railnet.quality()
                
            
    