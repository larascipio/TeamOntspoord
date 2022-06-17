from code.algorithms.random_algorithm import Make_Random_Routes
from code.classes.train import Train
import random
import sys

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
        self._max_dist = max_time

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
        route = Make_Random_Routes(self._railnet, max_trains, max_time)
        route.run()
        return route.get_trains()

    def run(self, iterations: int):

        # keep trying a random change and see if the score increases
        for _ in range(iterations):

            # qual = self.quality()
            sys.stdout.write(f'\rThe quality is {self.quality()}')
            sys.stdout.flush()

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
        # print(f'Extend {train}')
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
        # print(f'Now its {train}')

    def decrease_train(self, train):
        # print(f'Decrease {train}')

        # determine the quality
        qual_before = self.quality()

        # decrease the train at one of the ends
        index = random.choice([0,-1])
        connection = train.get_connections()[index]
        if index == 0:
            train.remove_first_connection()
        else:
            train.remove_last_connection()
        
        # determine the new quality
        qual_now = self.quality()

        # if the quality is better, keep the change
        if qual_now < qual_before:
            if index == 0:
                train.movestart(connection)
            else:
                train.move(connection)

        # remove trains with only one station
        if len(train.get_stations()) == 1:
            self.delete_train(train)

        # print(f'Now its {train}')


    def make_new_train(self):
        # print('Make new train')

        qual_before = self.quality()

        # choose a random connection to put a train on
        connection = random.choice(self._railnet.get_connections())

        connection.travel()
        qual_now = self.quality() - connection.get_distance() - 100
        connection.remove()

        if qual_now < qual_before:
            # print('Not worth it.')
            return

        new_train = Train(self._railnet, connection.get_destination(None), self._max_dist)
        new_train.move(connection)
        self._trains.append(new_train)
        # print(f'The new train is {new_train}')


    def split_train(self, train):
        # print(f'Split {train}')

        # determine the quality
        qual_before = self.quality()

        # see if removing this connection is worth it
        if len(train.get_stations()) < 4:
            # print('The train is too short.')
            return
        
        possible_connections = train.get_connections()[1:-1]

        if not possible_connections:
            return

        connection = random.choice(possible_connections)
        connection.remove()

        # the quality without this connection, but with an extra train
        qual_now = self.quality() + connection.get_distance() - 100
        connection.travel()

        if qual_now < qual_before:
            # print('Not worth it.')
            return

        # split the train
        connections = train.get_connections()

        # create a new train to replace the other one
        new_train = Train(self._railnet, train.get_stations()[0], self._max_dist)

        for current_connection in connections:

            # remove the connection from this train
            train.remove_first_connection()

            # check if this is the connection at which to split
            if current_connection == connection:
                break
                
            # move the new train
            new_train.move(current_connection)
        
        if len(new_train.get_stations()) > 1:
            self._trains.append(new_train)

        if len(train.get_stations()) < 2:
            self.delete_train(train)

        # print(f'This is now: {new_train}\nand {train}')


    def delete_train(self, train):
        if train in self._trains:
            self._trains.remove(train)
        else:
            raise Exception('You\'re trying to remove a train that does not exist.')