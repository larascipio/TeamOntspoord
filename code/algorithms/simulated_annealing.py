from code.algorithms.random_algorithm import Make_Random_Routes
from code.visualisation.plotly_animation import create_animation, create_gif
from code.visualisation.plotly_live import Live_Plot
# from code.classes.train import Train
import random
import sys

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
        # self._max_trains = max_trains
        # self._max_dist = max_time
        # self._max_trains = self._railnet.get_max_trains()
        # self._max_dist = self._railnet.get_max_distance()

        # needed for annealing
        self._iter = 0
        self._max_iter = 10000

    def keep_change(self, qual_before, qual_now) -> bool:
        """
        Returns true if the change made has increased the score.
        """
        if qual_now < qual_before:
            return False
        return True
    
    # def get_trains(self) -> list:
    #     return self._trains

    # def quality(self) -> float:
    #     """
    #     Calculate the quality of the current routes.
    #     """
    #     qual = (
    #         len(self._railnet.get_passed_connections())
    #         /self._railnet.get_total_connections()
    #         )*10000
    #     for train in self._trains:
    #         qual -= 100
    #         qual -= train.get_distance()
    #     return qual
    
    def get_random_routes(self):
        route = Make_Random_Routes(self._railnet)
        route.run()
        # # check
        # for train in route.get_trains():
            # if not len(train.get_stations()) == len(train.get_connections()) + 1:
            #     print('RANDOM ROUTES')
        # return self._railnet.get_trains()

    def run(self, iterations=100000):
        self._max_iter=iterations
        # gif = Live_Plot(self._railnet)

        # keep trying a random change and see if the score increases
        for self._iter in range(self._max_iter):

            # sys.stdout.write(f'\r{self._iter}')
            # sys.stdout.flush()

            # while len(self._trains) == 0:
            #     self.make_new_train(p=1)

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

            # create a gif:
            # gif.update_fig(self._iter)

            # # check
            # for train in self._railnet.get_trains():
            #     distance = 0
            #     for connection in train.get_connections():
            #         distance += connection.get_distance()
            #     if train.get_distance() != distance:
            #         raise Exception(f'The length of the train is {distance}, not {train.get_distance()}!')

        # print()
        # create_gif('hillclimber')
    
    def extend_train(self, train):
        # print(f'Extend {train}')
        # qual_before = self.quality()
        qual_before = self._railnet.quality()

        index = random.choice([0,-1])
        station = train.get_stations()[index]
        next_connection = random.choice(station.get_connections())

        if (train.get_distance() + next_connection.get_distance()) > self._railnet.get_max_distance():
            # print('The train is too long.')
            return

        if index == 0:
            train.movestart(next_connection)
        else:
            train.move(next_connection)
        
        # qual_now = self.quality()
        qual_now = self._railnet.quality()

        # check if the quality is better or worse
        if not self.keep_change(qual_before=qual_before, qual_now=qual_now):
            if index == 0:
                train.remove_first_connection()
            else:
                train.remove_last_connection()

        # print(f'Now its {train}')

        # # check
        # for connection in train.get_connections():
        #     if not connection.passed():
        #         print('extend_train')
        #         print(connection)
        #         print(train)
        #         raise Exception('it was extend_train')

    def decrease_train(self, train):
        # print(f'Decrease {train}')

        # determine the quality
        # qual_before = self.quality()
        qual_before = self._railnet.quality()

        # decrease the train at one of the ends
        index = random.choice([0,-1])
        connection_to_remove = train.get_connections()[index]
        if index == 0:
            train.remove_first_connection()
        else:
            train.remove_last_connection()
        
        # determine the new quality
        # qual_now = self.quality()
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

        # print(f'Now its {train}')

        # # check
        # for connection in train.get_connections():
        #     if not connection.passed():
        #         print('decrease_train')
        #         print(f'removed (or not) {connection_to_remove} at {index}')
        #         print()
        #         print(connection)
        #         print(train)
        #         raise Exception('it was decrease_train')

    def make_new_train(self,p=0):
        # print('Make new train')

        if len(self._railnet.get_trains()) == self._railnet.get_max_trains():
            # print('Too many trains.')
            return

        # qual_before = self.quality()
        qual_before = self._railnet.quality()

        # choose a random connection to put a train on
        connection = random.choice(self._railnet.get_connections())

        connection.travel()
        # qual_now = self.quality() - connection.get_distance() - 100
        qual_now = self._railnet.quality() - connection.get_distance() - 100
        connection.remove()

        # check if the quality is better or worse
        if not self.keep_change(qual_before=qual_before, qual_now=qual_now) and p == 0:
            # print('Not worth it.')
            return

        # new_train = Train(
        #     # routes=self._railnet, 
        #     starting_station=connection.get_destination(None), 
        #     max_distance=self._max_dist)
        starting_station = connection.get_destination(None)
        new_train = self._railnet.create_train(starting_station)
        new_train.move(connection)
        # self._trains.append(new_train)
        # print(f'The new train is {new_train}')


        # # check
        # for connection in new_train.get_connections():
        #     if not connection.passed():
        #         print(new_train)
        #         raise Exception('it was make_new_train')

    def split_train(self, train):
        # print(f'Split {train}')

        if len(self._railnet.get_trains()) == self._railnet.get_max_trains():
            # print('Too many trains.')
            return

        # determine the quality
        # qual_before = self.quality()
        qual_before = self._railnet.quality()

        # see if removing this connection is worth it
        if len(train.get_stations()) < 4:
            # print('The train is too short.')
            return
        
        connections = train.get_connections()

        index_to_split = random.randint(1, len(connections)-2)
        connection_to_split = connections[index_to_split]
        connection_to_split.remove()

        # the quality without this connection, but with an extra train
        # qual_now = self.quality() + connection.get_distance() - 100
        qual_now = self._railnet.quality() + connection_to_split.get_distance() - 100
        connection_to_split.travel()

        # check if the quality is better or worse
        if not self.keep_change(qual_before=qual_before, qual_now=qual_now):
            # print('Not worth it.')
            return

        # split the train

        # create a new train to replace the other one
        # new_train = Train(self._railnet, train.get_stations()[0], self._max_dist)
        new_train = self._railnet.create_train(train.get_stations()[0])

        # print(connections)
        # print(index_to_split)
        # print()

        for _ in range(index_to_split):
            # print(index)

            # remove the connection from this train
            connection = train.remove_first_connection()

            # move the new train
            new_train.move(connection)
            # print(connection)
            # print(f'This is now: {new_train}\nand {train}')
            # print()
        
        # remove the chosen connection
        train.remove_first_connection()
        
        # keep the new train if its longer than one station
        # if len(new_train.get_stations()) > 1:
        #     self._trains.append(new_train)

        if len(new_train.get_stations()) < 2:
            self._railnet.remove_train(new_train)

        # remove the old train if its shorter than one station
        if len(train.get_stations()) < 2:
            # self.delete_train(train)
            self._railnet.remove_train(train)

        # print(f'This is now: {new_train}\nand {train}')

        # check
        old_station = train.get_stations()[0]
        i = 0
        for new_station in train.get_stations()[1:]:
            if train.get_connections()[i].get_destination(old_station) != new_station:
                print(old_station, new_station)
                print(i, train.get_connections()[i])
                raise Exception('SPLIT INCORRECTLY')
            old_station = new_station
            i += 1
        
        for connection_to_split in train.get_connections():
            if not connection_to_split.passed():
                print('split_train')
                print(connection_to_split)
                print(train)
                raise Exception('it was split_train')


    def remove_train(self, train):
        # print(f'Remove {train}')
        # qual_before = self.quality()
        qual_before = self._railnet.quality()

        for connection in train.get_connections():
            connection.remove()
        
        # qual_now = self.quality() + train.get_distance() + 100
        qual_now = self._railnet.quality() + train.get_distance() + 100

        for connection in train.get_connections():
            connection.travel()

        if self.keep_change(qual_now=qual_now,qual_before=qual_before):
            # self.delete_train(train)
            self._railnet.remove_train(train)
            # print('Removed!')

        # # check
        # for connection in train.get_connections():
        #     if not connection.passed():
        #         print('remove_train')
        #         print(connection)
        #         print(train)
        #         raise Exception('it was remove_train')     

    # def delete_train(self, train):
    #     if train in self._trains:
    #         self._trains.remove(train)
    #     else:
    #         raise Exception('You\'re trying to remove a train that does not exist.')


class Simulated_Annealing(Hillclimber):
    def __init__(self, railnet, start_temp = 20, base=0.999):
        super().__init__(railnet)
        self._starttemp = start_temp
        self.temps = []
        self._base = base

    def keep_change(self, qual_before, qual_now):

        # check if a starting temperature is provided
        if self._starttemp == 0:
            raise Exception('Please provide a starting temperature if you\'re using simulated annealing.')

        # determine the temperature for this iteration
        # temp = 1
        # temp = self._starttemp - (self._starttemp/self._max_iter) * self._iter
        temp = self._starttemp * pow(self._base, self._iter)

        # print(temp)        

        # determine whether this change is kept
        qual_change = qual_now - qual_before
        # print(pow(2, qual_change)/temp)
        # print()
        if qual_change > 0:
            return True
        if temp == 0:
            return False
        elif pow(2, qual_change/temp) > random.random():
            return True
        return False

class Reheating(Hillclimber):
    """
    https://www.sciencedirect.com/science/article/pii/S0377221717300759?casa_token=JEj48ByZMJIAAAAA:bu5jvRf5EphHFiPSGWEodYny0K8gAqNqzpyHKZL93NKg_ysug9u30CTNJ2j7JndgfxkFmZIDVg
    """
    def __init__(self, railnet, start_temp=100, base=0.999):
        super().__init__(railnet)
        self._heat = 0 # current number of reheats
        self._bestqual = 0
        self._bestroute = None
        self._currentbest = 0
        
        self._temp = start_temp
        self._base = base
        self._stuck = 0
        
        self.temps = []
        self.best = []
        self.current = []
    
    def run(self):
        super().run()
        self._railnet.reset()
        self._railnet.restore_routes(self._bestroute)

    def keep_change(self, qual_before, qual_now) -> bool:

        self.temps.append(self._temp)
        self.best.append(self._bestqual)
        self.current.append(qual_before)

        # 10 times no changes
        if self._stuck > 50:
            self._heat += 1
            self._temp *= 2
            self._stuck = 0

        # determine whether this change is kept
        qual_change = qual_now - qual_before

        # positive changes are always accepted
        if qual_change > 0:
            if qual_now > self._bestqual:
                self._bestqual = qual_now
                self._bestroute = self._railnet.get_route_names()
            keep = True
            self._stuck = 0
        elif self._temp == 0:
            keep = False
        elif pow(2, qual_change/self._temp) > random.random():
            keep = True
            self._stuck = 0
        else:
            keep = False
            self._stuck += 1

        self._temp *= self._base
        return keep
