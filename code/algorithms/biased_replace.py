"""
biased_iteration.py

Programmeertheorie - minor programmeren
Lara, Tim, Eva

- Make a route then go over every train and try to find a superior replacement.
- No connection used more than once in the result.
- Uses the Railnet structure.
"""

import random

from code.algorithms.random_replace import Make_Replaced_Routes

class Make_Biased_Routes(Make_Replaced_Routes):
    def __init__(self, railnet):
        super().__init__(railnet)
        self._random = False
        self._current_station_weights = [1 for _ in range(self._railnet.get_total_stations())]

    def run(self, iterations=200):
        """
        Run the algorithm.
        """
        super().run(iterations=iterations)

    def create_train(self):
        """
        Create a new train at a random start station.
        """

        # choose random starting point
        start = random.choices(list(self._railnet.get_stations().values()),
                                weights=self._current_station_weights)[0]

        train = self._railnet.create_train(start)

        return train

    def change_tracks(self, iterations):
        for _ in range(self._railnet.get_max_trains()):

            # create a new weighted list
            self.precise_starter_locations()

            # find the best track for this train
            self.change_one_track(iterations)

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
        self._current_station_weights = weighted_chance_list


