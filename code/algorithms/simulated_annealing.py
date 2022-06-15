from code.algorithms.bad_algorithm import Make_Bad_Routes, Train
import random

class Hillclimber():
    def __init__(self, railnet, max_trains, max_time):
        self._railnet = railnet
        self._trains = self.get_random_routes(max_trains, max_time)
        self._changes = [
            self.extend_train, 
            self.decrease_train, 
            self.make_new_train, 
            self.split_train
        ]

    def quality(self) -> float:
        """
        Calculate the quality of the current routes.
        """
        qual = (len(self._railnet.get_passed_connections())/self._railnet.get_total_connections())*10000
        for train in self._trains:
            qual -= 100
            qual -= train.get_distance()
        return qual
    
    def get_random_routes(self, max_trains, max_time):
        route = Make_Bad_Routes(self._railnet, max_trains, max_time)
        route.run()
        return route.get_trains()

    def run(self, iterations):

        # keep trying a random change and see if the score increases
        for _ in range(iterations):

            # choose one of the trains
            train_to_change = random.choice(self._trains)

            # choose one of the possible changes
            change = random.choice(self._changes)

            if change == self.make_new_train:
                change()
            else:
                change(train_to_change)

            print()
    
    def extend_train(self, train):
        print(f'Extend {train}')
        qual_before = self.quality()
        index = random.choice([0,-1])
        station = train.get_stations()[index]
        next_connection = random.choice(station.get_connections())
        if index == 0:
            train.movestart(next_connection)
        else:
            train.move(next_connection)
            
        qual_now = self.quality()

        if qual_now < qual_before:
            if index == 0:
                train.remove_first_connection()
            else:
                train.remove_last_connection()
        print(f'Now its {train}')

    def decrease_train(self, train):
        print(f'Decrease {train}')
        qual_before = self.quality()
        index = random.choice([0,-1])
        connection = train.get_connections()[index]
        if index == 0:
            train.remove_first_connection()
        else:
            train.remove_last_connection()
        
        qual_now = self.quality()

        if qual_now < qual_before:
            if index == 0:
                train.movestart(connection)
            else:
                train.move(connection)
        print(f'Now its {train}')


    def make_new_train(self):
        print('Make new train')

    def split_train(self, train):
        print(f'Split {train}')
