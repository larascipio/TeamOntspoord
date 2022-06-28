"""
bad_algorithm.py

This algorithm creates routes for trains in which all connections of the provided railnetwork are passed.
There will never be more trains than the number provided and the trains will never exceed the distance provided.
"""

class Make_Greedy_Routes():
    def __init__(self, railnet):
        """
        Use network of routes to initialize the algorithm.
        """
        self._railnet = railnet

        # find the endstations
        self._end_stations = []
        for station in self._railnet.get_stations().values():
            if len(station.get_connections()) % 2 == 1:
                self._end_stations.append(station)

    def run(self):
        """
        Run the algorithm.
        """

        # keep creating trains untill all connections are passed
        while len(self._railnet.get_passed_connections()) < len(self._railnet.get_connections()):
            
            # check if there can be another train
            if len(self._railnet.get_trains()) == self._railnet.get_max_trains():
                return
            
            # create a train
            train = self.create_train()
            if not train:
                return

            # keep going until the route is 2 hours
            while train.is_running():
                # connection = train.choose_connection()
                connection = train.choose_next_connection()

                # stop this train if there are no more connections
                if not connection:
                    break

                # check if the train does not exceed the allowed distance
                if connection.get_distance() + train.get_distance() < self._railnet.get_max_distance():
                    train.move(connection)
                else:
                    train.stop()
            
            # remove the trains last station from the endstations
            if train.get_stations()[-1] in self._end_stations:
                self._end_stations.remove(train._current_station)

            print(self._railnet.get_trains())

    def create_train(self):
        """
        Create a train at a station.
        """

        # choose starting point
        start = None

        # keep going untill a starting point is found
        while not start:
            if len(self._end_stations) > 0:

            # choose one of the endstations
                start = self._end_stations.pop()
                
            else:
                # choose a random station that has not been travelled
                for station in self._railnet.get_stations().values():

                    # check if all connections are passed
                    if set(station.get_connections()) - self._railnet.get_passed_connections():
                        start = station
                        break
                
                # there are no stations left for new trains.
                return None

        # create the train
        return self._railnet.create_train(start)

    # def all_stations_passed(self) -> set:
    #     """
    #     Give a set of all stations passed.
    #     """
    #     stations = set()
    #     for train in self._route.get_trains.values():
    #         stations.add(train.get_stations())
    #     return stations

    # def quality(self) -> float:
    #     """
    #     Calculate the quality of the current routes.
    #     """
    #     qual = (len(self._railnet.get_passed_connections())/self._tot_connections)*10000
    #     for train in self._trains:
    #         qual -= 100
    #         qual -= train.get_distance()
    #     return qual

    def __repr__(self):
        representation = 'Route:\n'
        for train in self._trains:
            representation += f'{train}' + '\n'
        representation += f'quality = {self._railnet.quality()}'
        return representation
