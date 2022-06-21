import random
from code.classes.train import Train

# IDEEËN: check steeds de slechtste route en vervang die steeds
# Ga aan het eind langs de routes en verwijder de nutteloze
# Doe er wat restrictions bij, zodat de trein niet zomaar terugkeert langs dezelfde connecties en dezelfde stations
# BUGS: Follow Track voor structure.py werkt niet - lijkt uit zichzelf al deels te resetten
# In de train.py een set maken met connecties - sneller dan steeds langs de passed statement te loopen

class Make_Iterated_Routes():
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
    
    def run(self):
        """
        Run the algorithm.
        """
        # Create a random max distance (BIAS: not higher than input max distance)
        # self._random_distance = random.randint(1, self._max_dist)
        # set default iterations 
        for _ in range(self._max_trains):
            self.run_one_train()
        self.change_tracks(1)

    def run_one_train(self):

        train = self.create_train()

        if not train:
            return

        # keep going until the route is 2 hours
        while train.is_running():
            # connection = train.choose_connection()
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
            start = random.choice(self._possible_stations)

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

    # def changed_quality(self, trainlist):
    #     qual = (len(self._railnet.get_passed_connections())/self._tot_connections)*10000
    #     for train in trainlist:
    #         qual -= 100
    #         qual -= train.get_distance()
    #     return qual


    # def check_trains_quality(self):
    #     self.overall_quality = self.quality()
    #     print(self.overall_quality)
    #     iterated_train_list = []
    #     quality_list = []
    #     new_train_list = copy(self._trains)

    #     for train in self._trains:
    #         self._railnet.reset_train(train)
    #         new_train_list.remove(train)
        
    #         new_quality = self.changed_quality(new_train_list)
    #         quality_difference = new_quality - self.overall_quality
    #         # quality_dict[new_quality] = train
    #         iterated_train_list.append(train)
    #         new_train_list.append(train)
    #         quality_list.append(quality_difference)
    #         self._railnet.follow_train(train)
    #     print(len(iterated_train_list))
    #     return iterated_train_list, quality_list

    # def try_different_train(self, iterations):
    #     new_train_list = copy(self._trains)
    #     iterated_train_list, quality_list = self.check_trains_quality()
    #     print(quality_list, iterated_train_list)
    #     print('quality after the check')
    #     print(self.quality())

    #     i = 0
        
    #     for _ in range(self._max_trains):
    #         worst_train_dict = {}
    #         worst_train_quality = max(quality_list)
    #         highest_index = quality_list.index(worst_train_quality)
    #         worst_train = iterated_train_list[highest_index]
    #         del quality_list[highest_index]
    #         iterated_train_list.remove(worst_train)
    #         self.remove_train(worst_train)
    #         self._railnet.reset_train(worst_train)

    #         for _ in range(iterations):
    #             self.run_one_train()
    #             new_quality = self.quality()
    #             new_train = self._trains.pop()
    #             if new_quality > self.overall_quality:
    #                 worst_train_dict[new_quality] = new_train
    #             self._railnet.reset_train(new_train)
    #             i+=1

    #         if len(worst_train_dict) > 0:
    #             best_replacement = max(worst_train_dict)
    #             if best_replacement < worst_train_quality: # BETER DAN:
    #                 self._railnet.follow_train(worst_train)
    #                 self._trains.append(worst_train)
    #             elif worst_train_quality > self.overall_quality:
    #                 self._railnet.follow_train(worst_train_dict[best_replacement])
    #                 self._trains.append(worst_train_dict[best_replacement])
    #         else:
    #             self._railnet.follow_train(worst_train)
    #             self._trains.append(worst_train)
            
    #         print(self.quality())

    #     print(i)
    #     print(self.quality())
    #     print(self.overall_quality)
    #     print(len(self._trains))

    #     print(new_train_list)
    #     print('woohoo')
    #     print(self._trains)

    def change_tracks(self, iterations):

        the_very_first_quality = self.quality()

        for _ in range(self._max_trains):
            self._railnet.follow_track(self.get_trains())
            start_quality = self.quality()

            removed_train = self._trains[0]
            self._railnet.reset_train(removed_train)
            self.remove_train(removed_train)
            self._railnet.follow_track(self.get_trains())
            removed_quality = self.quality()

            worst_train_dict = {}

            for _ in range(iterations):
                self._railnet.follow_track(self.get_trains())
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

        # print(f'From {the_very_first_quality} to {best_replacement}')

        self._railnet.follow_track(self.get_trains())
        # print(f'{len(self._railnet.get_passed_connections())} connections passed out of {self._tot_connections}')


    def remove_train(self, train):
        self._railnet.reset_train(train)
        self._trains.remove(train)

    def __repr__(self):
        representation = 'Route:\n'
        for train in self._trains:
            representation += f'{train}' + '\n'
        representation += f'quality = {self.quality()}'
        return representation
