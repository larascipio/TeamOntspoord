"""
greedy_algorithm.py

Programmeertheorie - minor programmeren
Lara, Tim, Eva

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

    def create_train(self):
        """
        Create a train at a station.
        """

        # choose starting point
        if len(self._end_stations) > 0:

            # choose one of the endstations
            start = self._end_stations.pop()
            return self._railnet.create_train(start)

        else:
            # choose a random station that has not been travelled
            for station in self._railnet.get_stations().values():

                # check if there is a connection that has not been passed
                if set(station.get_connections()) - self._railnet.get_passed_connections():
                    return self._railnet.create_train(station)

        # there are no stations left for new trains.
        return None

    def __repr__(self):
        representation = 'Route:\n'
        for train in self._trains:
            representation += f'{train}' + '\n'
        representation += f'quality = {self._railnet.quality()}'
        return representation
