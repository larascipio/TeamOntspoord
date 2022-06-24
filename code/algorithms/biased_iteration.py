import random

class Make_Biased_Routes():
    def __init__(self, railnet):
        """
        Create a train at the given station.
        """
        self._railnet = railnet
        self._possible_stations = list(self._railnet.get_stations().values())
        

    # def starter_locations(self):
    #     weighted_chance_list = []
    #     for station in self._railnet.get_stations():
    #         weighted_chance = len(station.get_connections())
    #         if weighted_chance > 0:
    #             weighted_chance = 1 / weighted_chance
    #         weighted_chance_list.append(weighted_chance)
    #     return weighted_chance_list

    def precise_starter_locations(self):
        """
        Get starter locations with connections that haven't been passed through.
        Give preference to stations with few connections, so connections near the edge
        will be used.
        """

        weighted_chance_list = []
        for station in self._railnet.get_stations().values():
            weighted_chance = 0
            if len(station.get_connections()) > 0:
                for connection in station.get_connections():
                    if connection.passed():
                        weighted_chance += 1
                if weighted_chance > 0:
                    weighted_chance = 1 / weighted_chance
            weighted_chance_list.append(weighted_chance)
        return weighted_chance_list
    
    def run(self):
        """
        Run the algorithm.
        """
        # Create a random max distance (BIAS: not higher than input max distance)
        # self._random_distance = random.randint(1, self._max_dist)
        for _ in range(self._railnet.get_max_trains()):
            weighted_chance_list = self.precise_starter_locations()
            self.run_one_train(weighted_chance_list)
        self.change_tracks(250)
        # self.change_worst_train(iterations)

    def run_one_train(self, weighted_chance_list):
        """
        Create and run one train
        """
        train = self.create_weighted_train(weighted_chance_list)

        if not train:
            return

        # keep going until the route is 2 hours
        while train.is_running():
            # connection = train.choose_connection()
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
        # weighted_chance_list = self.precise_starter_locations()
        # choose random starting point
        while not start:
            start = random.choices(self._possible_stations, weights=weighted_chance_list, k=1)
            start = start[0]
        
        train = self._railnet.create_train(start)
        return train

    # def change_worst_train(self, iterations):
        
    #     iterated_train_list, quality_list = self._railnet.check_trains_quality()
    #     worst_train_index = quality_list.index(max(quality_list))
    #     worst_train = iterated_train_list[worst_train_index]

    #     self.change_one_track(worst_train, iterations)

    def change_one_track(self, removed_train, iterations):

        start_quality = self._railnet.quality()

        self._railnet.remove_train(removed_train)
        removed_quality = self._railnet.quality()

        if removed_quality > start_quality:
            best_quality = removed_quality
        else:
            best_quality = start_quality
            best_replacement = removed_train

        weighted_chance_list = self.precise_starter_locations()

        for _ in range(iterations):
            self.run_one_train(weighted_chance_list)
            new_quality = self._railnet.quality()
            new_train = self._railnet.get_trains()[-1]
            self._railnet.remove_train(new_train)
            
            if new_quality > best_quality:
                best_quality = new_quality
                best_replacement = new_train

        if best_quality > removed_quality:
            self._railnet.add_train(best_replacement)

    def change_tracks(self, iterations):

        # the_very_first_quality = self._railnet.quality()

        for _ in range(self._railnet.get_max_trains()):
            removed_train = self._railnet.get_trains()[0]
            self.change_one_track(removed_train, iterations)
            
        # print(f'From {the_very_first_quality} to {self._railnet.quality()}')
        # print(f'{len(self._railnet.get_passed_connections())} connections passed out of {self._railnet.get_total_connections()}')

    # def __repr__(self):
    #     representation = 'Route:\n'
    #     for train in self._trains:
    #         representation += f'{train}' + '\n'
    #     representation += f'quality = {self.quality()}'
    #     return representation
