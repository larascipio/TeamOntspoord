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
    
    def create_train(self):
        """
        Create a new train at a random start station.
        """
        start = random.choice(list(self._railnet.get_stations().values()))

        train = self._railnet.create_train(start)

        return train
    
    def run(self):
        """
        Run the algorithm.
        """

        # Create a random amount of trains (at least 1) within the constraint
        self._random_amount = random.randint(1, self._railnet.get_max_trains())

        for _ in range(self._random_amount):
            train = self.create_train()
            self.run_one_train(train)

    def run_one_train(self, train):
        """
        Run a single train.
        """

        # Keep going until the max time is achieved
        while train.is_running():

            connection = train.choose_random_connection()

            if not connection:
                break

            if connection.get_distance() + train.get_distance() < self._railnet.get_max_distance():
                train.move(connection)
            else:
                train.stop()