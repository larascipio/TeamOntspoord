import random
from .bad_algorithm import Make_Bad_Routes
from code.classes.train import Train
import random

class Depth_First():
    """
    A Depth First search algorithm.
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
        self._best_route = None
        self._start_quality = 0

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

# Check if different route can be made with same start station, otherwise choose next station 

# if more than 2 stations: check quality

# if quality is worse than already existent quality, dont continue, otherwise continue 
    def compare_quality(self, route):
        new_value = quality()
        old_value = self._start_quality

        if new_value >= old_value:
            self.best_route = route
            self._start_quality = new_value
            print(f"New best value: {self.best_value}")

    def quality(self) -> float:
        """
        Calculate the quality of the current routes.
        """
        qual = (
            len(self._railnet.get_passed_connections())
            /self._railnet.get_total_connections()
            )*10000
        for train in self._trains:
            qual -= 100
            qual -= train.get_distance()
        return qual

    def run(self):
        """
        Run the algorithm.
        """

        # Create the input amount of trains 
        for _ in range(self._max_trains):
            # create a train
            train = self.create_train()

            if not train:
                return

        # Keep going until the route is 2 hours
            while train.is_running():
                connection = train.choose_first_connection()

                if not connection:
                    break

                if connection.get_distance() + train.get_distance() < self._max_dist:
                    # calculate quality up to this point 
                    quality = quality()
                    # check if its already better than highest quality 
                    if quality >= self._start_quality:
                        self._start_quality = quality 
                        train.move(connection)
                else:
                    train.stop()

        # Save the train
            self._trains.append(train)    