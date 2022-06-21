import random
from code.classes.train import Train

# Check if a connection one step away can be used and if that is preferable

class Make_Biased_Routes():
    def __init__(self, railnet, num_trains: int, max_distance: int):
        """
        Create a train at the given station.
        """
        self._railnet = railnet
        self._max_trains = num_trains
        self._max_dist = max_distance
        self._tot_stations = len(self._railnet.get_stations())
        self._tot_connections = len(self._railnet.get_connections())
        self._trains = []
        self._possible_stations = []
        for station in self._railnet.get_stations().values():
            self._possible_stations.append(station)

    # def starter_locations(self):
    #     weighted_chance_list = []
    #     for station in self._railnet.get_stations():
    #         weighted_chance = len(station.get_connections())
    #         if weighted_chance > 0:
    #             weighted_chance = 1 / weighted_chance
    #         weighted_chance_list.append(weighted_chance)
    #     return weighted_chance_list

    def precise_starter_locations(self):
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
    
    def run(self, iterations):
        """
        Run the algorithm.
        """
        # Create a random max distance (BIAS: not higher than input max distance)
        # self._random_distance = random.randint(1, self._max_dist)
        for _ in range(self._max_trains):
            self.run_one_train()
        self.change_tracks(iterations)
        # self.change_worst_train(iterations)

    def run_one_train(self):
        train = self.create_weighted_train()

        if not train:
            return

        # keep going until the route is 2 hours
        while train.is_running():
            # connection = train.choose_connection()
            connection = train.choose_next_connection()

            if not connection:
                break

            if connection.get_distance() + train.get_distance() < self._max_dist:
                train.move(connection)
            else:
                train.stop()

        # save the train
        self._trains.append(train)
    
    def create_weighted_train(self):
        """
        Create a new train at a random start station.
        """
        start = None
        weighted_chance_list = self.precise_starter_locations()
        # choose random starting point
        while not start:
            start = random.choices(self._possible_stations, weights=weighted_chance_list, k=1)
            start = start[0]

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


    def check_trains_quality(self):
        """
        Check how each train affects the quality. 
        Store in two lists so duplicate scores aren't overwritten.
        The higher the quality difference, the more negatively the train affects the quality
        """
        self.overall_quality = self.quality()
        iterated_train_list = []
        quality_list = []

        for train in self._trains:
            self._railnet.reset_train(train)
            self._trains.remove(train)

            quality_difference = self.quality() - self.overall_quality
            # quality_dict[new_quality] = train
            iterated_train_list.append(train)
            quality_list.append(quality_difference)

            self._railnet.follow_train(train)
            self._trains.append(train)

        return iterated_train_list, quality_list

    def change_worst_train(self, iterations):
        
        iterated_train_list, quality_list = self.check_trains_quality()
        worst_train_index = quality_list.index(max(quality_list))
        worst_train = iterated_train_list[worst_train_index]

        self.change_one_track(worst_train, iterations)

    def change_one_track(self, removed_train, iterations):

        start_quality = self.quality()

        self._railnet.reset_train(removed_train)
        self._trains.remove(removed_train)
        removed_quality = self.quality()

        worst_train_dict = {}

        for _ in range(iterations):
            self.run_one_train()
            new_quality = self.quality()
            new_train = self._trains.pop()
            
            if new_quality > start_quality and new_quality > removed_quality:
                worst_train_dict[new_quality] = new_train
            self._railnet.reset_train(new_train)

        if len(worst_train_dict) > 0:
            best_replacement = max(worst_train_dict)
            self._railnet.follow_train(worst_train_dict[best_replacement])
            self._trains.append(worst_train_dict[best_replacement])
        elif removed_quality < start_quality:
            self._railnet.follow_train(removed_train)
            self._trains.append(removed_train)

    def change_tracks(self, iterations):

        the_very_first_quality = self.quality()

        for _ in range(self._max_trains):
            removed_train = self._trains[0]
            self.change_one_track(removed_train, iterations)
            
        print(f'From {the_very_first_quality} to {self.quality()}')
        print(f'{len(self._railnet.get_passed_connections())} connections passed out of {self._tot_connections}')

    def __repr__(self):
        representation = 'Route:\n'
        for train in self._trains:
            representation += f'{train}' + '\n'
        representation += f'quality = {self.quality()}'
        return representation
