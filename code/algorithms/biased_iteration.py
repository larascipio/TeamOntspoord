"""
biased_iteration.py

Programmeertheorie - minor programmeren
Lara, Tim, Eva

- Make a route then go over every train and
    try to find a superior replacement.
- No connection used more than once in the result.
- Uses the Railnet structure.
"""

import random


class Make_Biased_Routes():
    def __init__(self, railnet):
        """
        Create a train at the given station.
        """
        self._railnet = railnet
        self._possible_stations = list(self._railnet.get_stations().values())

    def precise_starter_locations(self):
        """
        Get starter locations with connections that haven't been passed through.
        """
        weighted_chance_list = []
        for station in self._railnet.get_stations().values():
            weighted_chance = 0
            # only use stations that have yet to be passed connections
            for connection in station.get_connections():
                if connection.passed():
                    weighted_chance += 1
            if weighted_chance > 0:
                # give preference to stations with few connections
                weighted_chance = 1 / weighted_chance
            weighted_chance_list.append(weighted_chance)
        return weighted_chance_list

    def run(self):
        """
        Run the algorithm.
        """
        for _ in range(self._railnet.get_max_trains()):
            weighted_chance_list = self.precise_starter_locations()
            train = self.create_weighted_train(weighted_chance_list)
            self.run_one_train(train)

        # no significant improvement beyond 200 iterations
        self.change_tracks(200)

    def run_one_train(self, train):
        """
        Create and run one train
        """

        if not train:
            return

        # keep going until the route is the max distance
        while train.is_running():

            connection = train.choose_next_connection()

            if not connection:
                break

            if connection.get_distance() + train.get_distance() < self._railnet.get_max_distance():
                train.move(connection)
            else:
                train.stop()

    def create_weighted_train(self, weighted_chance_list):
        """
        Create a new train at a random start station.
        """
        start = None

        # choose random starting point
        while not start:
            start = random.choices(list(self._railnet.get_stations().values()),
                                   weights=weighted_chance_list, k=1)
            start = start[0]

        train = self._railnet.create_train(start)
        return train

    def change_one_track(self, removed_train, iterations):
        """
        Create trainroutes and replace
        the current train if preferable.
        """

        # quality with the train
        start_quality = self._railnet.quality()

        # quality without the train
        self._railnet.remove_train(removed_train)
        removed_quality = self._railnet.quality()

        # save best quality as best quality
        if removed_quality > start_quality:
            best_quality = removed_quality
        else:
            best_quality = start_quality
            best_replacement = removed_train

        # get starter positions for the trains
        weighted_chance_list = self.precise_starter_locations()

        # create the new trains and save the best one
        for _ in range(iterations):
            train = self.create_weighted_train(weighted_chance_list)
            self.run_one_train(train)
            new_quality = self._railnet.quality()
            new_train = self._railnet.get_trains()[-1]
            self._railnet.remove_train(new_train)

            if new_quality > best_quality:
                best_quality = new_quality
                best_replacement = new_train

        # put the best train into the railnet
        if best_quality > removed_quality:
            self._railnet.add_train(best_replacement)

    def change_tracks(self, iterations):
        """
        Iterate over every single train and possibly replace them.
        """

        for _ in range(self._railnet.get_max_trains()):
            removed_train = self._railnet.get_trains()[0]
            self.change_one_track(removed_train, iterations)
