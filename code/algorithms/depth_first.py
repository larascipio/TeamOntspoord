from opcode import stack_effect
from code.algorithms.random_algorithm import Make_Random_Routes
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
        route.run()

    def get_next_train(self):
        """
        Method that returns the first train station of traject.
        """
        if len(self._copy_railnet_trains) > 0:
            return self._copy_railnet_trains.pop()
  
    def build_trains(self):
        """
        Creates all possible trajects from a single start station and returns them in a list of stations.
        """

        list_of_trains = []
<<<<<<< HEAD
        stack = [start_station]
        print(f'Start {stack}')
        
        while stack:
            print(f'Stack: {stack}')
            station = stack.pop()
            # new_train = self._copy_railnet.create_train(station)
            
            # if station not in path:
            #     path.append(station)
                
=======
        # aangepast naar current train
        stack = [self._current_train]
        print(f'Start {stack}')
        
        while stack:
            train = stack.pop()
             # Dit nog aanpassen, train.next_connection? 
>>>>>>> 9ccaa12b818b01d5e7df30d2493a5dcc4c046d71
            for connection in station.get_connections():
                station = connection._stations[1]
                if not station._passed:
                    stack.append(station)
                    station._passed = True
                print(f'possible {stack}')
            train = copy.deepcopy(stack)
            #print(f'possible {train}')
            station_names = []
            for station in train:
                station_names.append(station._name)
            if len(station_names) > 0:
                list_of_trains.append(station_names)
        print(list_of_trains)
            #print(list_of_trains)
        return list_of_trains

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

        create_animation(self._railnet)

        # save initial quality of the train network
        self._old_quality = self._quality

        # Copy train network to delete and change trains
        self._copy_railnet = copy.deepcopy(self._railnet)
        # print(f'Old {self._copy_railnet}')

        self._copy_railnet_trains = list(self._copy_railnet.get_trains())
        # print(f'copy_railnet_trains: {self._copy_railnet_trains}')

        # Go through every train of the railnet
        while self._copy_railnet_trains: # TODO waarom maak je hier niet gewoon een for-loop van?

            # Take a train apart to search depth first 
            self._current_train = self.get_next_train()

            # Return all possible trains from same start station 
            possible_trains = self.build_trains()

            # Delete the train from train network 
            self._copy_railnet.remove_train(self._current_train)

            # Select the start station to create all the routes from
            #start_station = self._current_train.get_stations()[0]
            
            # Return all possible trains from same start station 
            #possible_trains = self.build_trains(start_station)
            #print(f'TRAINS {self._trains}')
            #print(f'possible {possible_trains}')

            # Find and replace the best train found 
            self._best_train = self.find_and_replace_best_train(possible_trains)
            #print(f'best {self._best_train}')
            
            # Add best train to railnet 
            self._copy_railnet.add_train(self._best_train)

<<<<<<< HEAD
            break # TODO weghalen voor meer treinen

        # print(f'New {self._copy_railnet}')
=======
        print(f'New {self._copy_railnet}')
>>>>>>> 9ccaa12b818b01d5e7df30d2493a5dcc4c046d71
