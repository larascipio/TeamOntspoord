import random
from code.classes.train import Train

class Make_Random_Routes():
    """
    The random algorithm creates random connections with a random amount of trains, 
    in which the end of a connection is depending on weights and random choice.
    """
    def __init__(self, railnet, num_trains: int, max_distance: int):
        """
        Use network of routes to initialize the algorithm.
        """
        self._railnet = railnet
        self._max_trains = num_trains
        self._max_dist = max_distance
        self._tot_connections = len(self._railnet.get_connections())
        self._trains = []
    
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

        return Train(self._railnet, start, self._max_dist)
    
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
    
    def run(self):
        """
        Run the algorithm.
        """

        # Create a random amount of trains within the constraint (BIAS: 0 = eruit )
        self._random_amount = random.randint(1, self._max_trains)
        for _ in range(self._random_amount):
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