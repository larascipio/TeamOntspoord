from code.algorithms.bad_algorithm import Train
import random

class Hillclimber():
    def __init__(self, railnet):
        self._rails = railnet
        self._trains = self.get_random_routes()
        self._changes = [] # TODO list of function for changes
    
    def get_random_routes(self):
        return []

    def run(self, iterations):

        # keep trying a random change and see if the score increases
        for _ in iterations:

            # choose one of the trains
            train_to_change = random.choice(self._trains)

            # choose one of the possible changes
            change = random.choice(self._changes)

            # the changes include extending a train on either end, 
            # decreasing a train on either end,
            # adding a new train on a connection (only station only decreases score)
            # splitting a train in two

            # removing a train that is only one station (al bij decreasing?)

            # get the score

            train_to_change.change()

            # get the new score

            # move back if the score is now lower
            

    def transformation(self):
        pass

class Climbing_Train(Train):
    def __init__(self, train):
        pass