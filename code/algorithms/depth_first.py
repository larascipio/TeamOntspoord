import random
from code.algorithms.random_algorithm import Make_Random_Routes
from code.classes.train import Train
import random

class Depth_First():
    """
    A Depth First search algorithm.
    """

    def __init__(self, railnet):
        """
        Use network of routes to initialize the algorithm.
        """
        self._railnet = railnet
        self._graph = {}
        for i in self._railnet._stations:
            self._graph[i] = self._railnet._stations[i].get_connections()
        print(self._graph)
        self._possible_stations = list(self._railnet.get_stations().values())

        self._max_trains = self._railnet.get_max_trains()
        self._max_dist = self._railnet.get_max_distance()
        self._best_route = None
        self._start_quality = 0

    # def get_next_state(self):
    #     return self._possible_stations.pop()

    # def create_train(self):
    #     """
    #     Create a new train at a random start station.
    #     """
    #     start = None
    #     # choose random starting point
    #     while not start:
    #         # choose a random start station 
    #         start = random.choice(self._possible_stations)

    #     train = self._railnet.create_train(start)
    #     return train

    # def search_depth_first(self):
    #     stack = [] 
    #     depth = 10
    #     while len(stack) > 0:
    #         state = stack.pop()
    #         if len(state) < depth:
    #             for i in [state]:
    #                 child = state
    #                 child += i
    #                 stack.append(child)
    

    # def compare_quality(self, route): 
    #     pass 
    #     new_value = quality()
    #     old_value = self._start_quality

    #     if new_value >= old_value:
    #         self.best_route = route
    #         self._start_quality = new_value
    #         print(f"New best value: {self.best_value}")\
    #         return True
    #     return False

    # def quality(self) -> float:
    #     """
    #     Calculate the quality of the current routes.
    #     """
    #     qual = (
    #         len(self._railnet.get_passed_connections())
    #         /self._railnet.get_total_connections()
    #         )*10000
    #     for train in self._trains:
    #         qual -= 100
    #         qual -= train.get_distance()
    #     return qual

    # def run(self):
    #     """
    #     Run the algorithm.
    #     """

    #     # Create the input amount of trains 
    #     for _ in range(self._max_trains):
    #         # create a train
    #         train = self.create_train()
    #         if not train:
    #             return

    #     # Keep going until the route is 2 hours
    #         while train.is_running():
    #             search_depth_first(train)


    #             if not connection:
    #                 break

    #             if connection.get_distance() + train.get_distance() < self._max_dist:
    #                 # Waar sla ik die route tussentijds op?
    #                 # Bereken quality 
    #                 # Bereken quality zonder alle connections? Met 1 trein? 
    #                 if compare_quality(route): 
    #                     train.move(connection)
    #             else:
    #                 train.stop()

    #     # Save the train
    #         self._trains.append(train)    