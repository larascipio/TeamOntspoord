import random
from code.algorithms.random_algorithm import Make_Random_Routes
from code.classes.train import Train
import random

class Make_New_Routes():
    def __init__(self, railnet, num_trains: int, max_distance: int):
        """
        Create a train at the given station.
        """
        self._railnet = railnet
        self._max_trains = num_trains
        self._max_dist = max_distance
        self._tot_connections = len(self._railnet.get_connections())
        self._trains = []
    
    def run_with_n_trains(self):
        for n in range(self._max_trains):
            self.n_of_trains = n
            print(self.n_of_trains)
            self.run()

    def run(self):
        """
        Run the random algorithm.
        """

        # Create a random amount of trains within the constraint
        for _ in range(self.n_of_trains):
            # create a train
            train = self.create_train()

            if not train:
                return

        # keep going until the route is 2 hours
            while train.is_running():
                connection = train.choose_random_connection()

                if not connection:
                    break

                if connection.get_distance() + train.get_distance() < self._max_dist:
                    train.move(connection)
                else:
                    train.stop()

        # save the train
            self._trains.append(train)
    
    def create_train(self):
        """
        Create a new train at a random start station.
        """
        start = None
        # choose random starting point
        while not start:
            # choose a random start station 
            possible_stations = []
            for station in self._railnet.get_stations().values():
                possible_stations.append(station)
            start = random.choice(possible_stations)

        return Train(self, start, self._max_dist)
    
    def get_trains(self):
        return self._trains
    
    def quality(self) -> float:
        """
        Calculate the quality of the current routes.
        """
        qual = (len(self._railnet.get_passed_connections())/self._tot_connections)*10000
        for train in self._trains:
            qual -= 100
            qual -= train.get_distance()
        return qual

    def __repr__(self):
        representation = 'Route:\n'
        for train in self._trains:
            representation += f'{train}' + '\n'
        representation += f'quality = {self.quality()}'
        return representation
    