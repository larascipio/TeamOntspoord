"""
simulated_annealing.py

Programmeertheorie - minor programmeren
Lara, Tim, Eva

- Houses the algorithms for the hillclimber, simulated annealing and reheating.
- Uses the Railnet structure.
- Uses the random algorithm to create starting routes.
"""

# ------------------------------- Imports --------------------------------------

from code.algorithms.random_algorithm import Make_Random_Routes
import random

# ------------------------------- Hillclimber ----------------------------------


class Hillclimber():
    def __init__(self, railnet):
        """
        Initialize the hillclimber algorithm.
        """
        self._railnet = railnet
        self.get_random_routes()
        self._changes = [
            self.extend_train,
            self.decrease_train,
            self.make_new_train,
            self.split_train,
            self.remove_train
        ]

        self._bestqual = 0
        self._bestroute = None

    def get_random_routes(self):
        """Use the random algorithm to get routes to start with."""
        route = Make_Random_Routes(self._railnet)
        route.run()

    def run(self, iterations=100000):
        """
        Run the algorithm for the provided amount of iterations.
        If no amount is provided, the algorithm will run for 100000 iterations.
        """
        self._max_iter = iterations

        # keep trying a random change and see if the score increases
        for self._iter in range(self._max_iter):

            # if there are no trains, make one
            while len(self._railnet.get_trains()) == 0:
                self.make_new_train(p=1)

            # choose one of the trains
            train_to_change = random.choice(self._railnet.get_trains())

            # choose one of the possible changes
            change = random.choice(self._changes)

            if change == self.make_new_train:
                change()
            else:
                change(train_to_change)

            # check if this route is better than the best route till now
            if self._railnet.quality() > self._bestqual:
                self._bestqual = self._railnet.quality()
                self._bestroute = self._railnet.get_route_names()

    def keep_change(self, qual_before, qual_now) -> bool:
        """
        Returns true if the change made has increased the score.
        """
        if qual_now < qual_before:
            return False
        return True

    def extend_train(self, train):
        """Extend the train at one of the ends."""

        # save the quality before the change
        qual_before = self._railnet.quality()

        # pick which end to extend over which connection
        index = random.choice([0, -1])
        station = train.get_stations()[index]
        next_connection = random.choice(station.get_connections())

        # check if the train does not get too long
        if (train.get_distance() + next_connection.get_distance()) > self._railnet.get_max_distance():
            return

        # extend the train
        if index == 0:
            train.movestart(next_connection)
        else:
            train.move(next_connection)

        # save the quality after the change
        qual_now = self._railnet.quality()

        # check if the quality is better or worse
        if not self.keep_change(qual_before=qual_before, qual_now=qual_now):

            # return to the state before the change
            if index == 0:
                train.remove_first_connection()
            else:
                train.remove_last_connection()

    def decrease_train(self, train):
        """Decrease the train at one of the ends."""

        # determine the quality
        qual_before = self._railnet.quality()

        # decrease the train at one of the ends
        index = random.choice([0, -1])
        connection_to_remove = train.get_connections()[index]
        if index == 0:
            train.remove_first_connection()
        else:
            train.remove_last_connection()

        # determine the new quality
        qual_now = self._railnet.quality()

        # if the quality is better, keep the change
        if not self.keep_change(qual_before=qual_before, qual_now=qual_now):
            if index == 0:
                train.movestart(connection_to_remove)
            else:
                train.move(connection_to_remove)

        # remove trains with only one station
        if len(train.get_stations()) == 1:
            # self.delete_train(train)
            self._railnet.remove_train(train)

    def make_new_train(self, p=0):
        """Make a new train at a random connection."""

        if len(self._railnet.get_trains()) == self._railnet.get_max_trains():
            # The maximum train limit has been reached.
            return

        # save the quality before
        qual_before = self._railnet.quality()

        # choose a random connection to put a train on
        connection = random.choice(self._railnet.get_connections())
        connection.travel()

        # save the quality now
        qual_now = self._railnet.quality() - connection.get_distance() - 100

        # return to the state before the change
        connection.remove()

        # check if the quality is better or worse
        if not self.keep_change(qual_before=qual_before, qual_now=qual_now) and p == 0:
            # the change is not worth it
            return

        # create a new train at the given connection
        starting_station = connection.get_destination(None)
        new_train = self._railnet.create_train(starting_station)
        new_train.move(connection)

    def split_train(self, train):
        """Split the train at a random connection"""

        if len(self._railnet.get_trains()) == self._railnet.get_max_trains():
            # The maximum train limit has been reached.
            return

        # save the quality before
        qual_before = self._railnet.quality()

        # check if the train can be split
        if len(train.get_stations()) < 4:
            return

        # choose at which connection to split the train
        connections = train.get_connections()
        index_to_split = random.randint(1, len(connections)-2)
        connection_to_split = connections[index_to_split]
        connection_to_split.remove()

        # save the quality now
        qual_now = self._railnet.quality() + connection_to_split.get_distance() - 100

        # return to the state before the change
        connection_to_split.travel()

        # check if the quality is better or worse
        if not self.keep_change(qual_before=qual_before, qual_now=qual_now):
            return

        # split the train

        # create a new train to replace the other one
        new_train = self._railnet.create_train(train.get_stations()[0])

        # move the new train till the chosen connection
        for _ in range(index_to_split):

            # remove the connection from this train
            connection = train.remove_first_connection()

            # move the new train
            new_train.move(connection)

        # remove the chosen connection from the original train
        train.remove_first_connection()

        # check if the trains are longer than 1 station
        if len(new_train.get_stations()) < 2:
            self._railnet.remove_train(new_train)

        if len(train.get_stations()) < 2:
            self._railnet.remove_train(train)

    def remove_train(self, train):
        """Remove a train"""

        # save the quality before
        qual_before = self._railnet.quality()

        # remove all connections
        for connection in train.get_connections():
            connection.remove()

        # save the quality now
        qual_now = self._railnet.quality() + train.get_distance() + 100

        # return to the state before the change
        for connection in train.get_connections():
            connection.travel()

        # check if the quality is better or worse
        if self.keep_change(qual_now=qual_now, qual_before=qual_before):
            self._railnet.remove_train(train)


class Simulated_Annealing(Hillclimber):
    def __init__(self, railnet, start_temp: int = 20):
        """Initialize the simulated annealing algorithm."""
        super().__init__(railnet)
        self._starttemp = start_temp
        self.temps = []

        # check if a valid starting temperature is provided
        if self._starttemp <= 0:
            raise Exception('Please provide a positive, nonzero starting temperature.')

    def keep_change(self, qual_before, qual_now):
        """Determines whether to keep the change based on a linear temperature decrease."""

        # determine the temperature for this iteration
        temp = self._starttemp - (self._starttemp/self._max_iter) * self._iter
        # temp = self._starttemp * pow(self._base, self._iter)

        # determine whether this change is kept
        qual_change = qual_now - qual_before
        if qual_change > 0:
            # positive changes are always accepted
            return True
        elif temp == 0:
            # if the temperature is zero, the change is always rejected
            return False
        elif pow(2, qual_change/temp) > random.random():
            return True
        return False


class Reheating(Hillclimber):
    """
    The inspiration for this algorithm can be found at:
    https://doi.org/10.1016/j.ejor.2017.01.040
    This algorithm was heavily simplified for this version of reheating.
    """
    def __init__(self, railnet, start_temp=100, base=0.9994):
        """Initialize the reheating algorithm."""

        super().__init__(railnet)

        self._heat = 0
        self._temp = start_temp
        self._base = base
        self._stuck = 0
        self._threshold = 50

    def run(self, iterations=50000):
        """Run the algorithm"""
        super().run(iterations)

        print(self._bestroute)

        # reset the best route after running the algorithm
        self._railnet.reset()
        self._railnet.restore_routes(self._bestroute)

    def keep_change(self, qual_before, qual_now) -> bool:

        # reheat after the algorithm has not changed for a while
        if self._stuck > self._threshold:

            # count the number of heats
            self._heat += 1

            # increase the temperature
            self._temp *= 2

            # reset the stuck-counter
            self._stuck = 0

        # determine whether this change is kept
        qual_change = qual_now - qual_before
        if qual_change > 0:

            # positive changes are always accepted
            keep_change = True
        elif self._temp == 0:

            # if the temperature is zero, the change is always rejected
            keep_change = False
        elif pow(2, qual_change/self._temp) > random.random():

            # a negative change is accepted
            keep_change = True
        else:

            # no change is made
            keep_change = False

        # decrease the temperature
        self._temp *= self._base

        # check if the algorithm is changed or not
        if keep_change:
            self._stuck = 0
        else:
            self._stuck += 1

        return keep_change
