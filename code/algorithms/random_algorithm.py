"""
random_algorithm.py

Programmeertheorie - minor programmeren
Lara, Tim, Eva

- Houses the random algorithm that is used by random iteration,
    hillclimber, simultaneous annealing and reheating.
- Uses the Railnet structure.
"""

import random


class Make_Random_Routes():
    """
    The random algorithm creates random connections with a random amount of trains,
    in which the end of a connection is depending on weights and random choice.
    """
    def __init__(self, railnet):
        """
        Use network of routes to initialize the algorithm.
        """
        self._railnet = railnet
        self._random = True

    def run(self):
        """
        Run the algorithm.
        """
        # create a random amount of trains (at least 1) within the constraint
        self._random_amount = random.randint(1, self._railnet.get_max_trains())

        # make a train network
        for _ in range(self._random_amount):
            self.run_one_train()

    def create_train(self):
        """
        Create a new train at a random start station.
        """
        # choose a random station
        start = random.choice(list(self._railnet.get_stations().values()))

        train = self._railnet.create_train(start)

        return train

    def run_one_train(self):
        """
        Run a single train.
        """

        train = self.create_train()

        # keep adding stations until the max time is reached
        while train.is_running():

            if self._random:
                connection = train.choose_random_connection()
            else:
                connection = train.choose_next_connection()
    
            if not connection:
                break

            # check if a move is possible
            if connection.get_distance() + train.get_distance() < self._railnet.get_max_distance():
                train.move(connection)
            else:
                train.stop()
