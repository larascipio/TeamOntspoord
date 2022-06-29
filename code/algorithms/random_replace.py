"""
random_iteration.py

Programmeertheorie - minor programmeren
Lara, Tim, Eva

- Make a random route, then go over every train and
    try to find a superior replacement.
- Uses the Railnet structure.
- Uses the random algorithm to create routes.
"""

from code.algorithms.random_algorithm import Make_Random_Routes


class Make_Replaced_Routes(Make_Random_Routes):

    def run(self, iterations=1000):
        """
        Run the algorithm.
        """
        for _ in range(self._railnet.get_max_trains()):
            self.run_one_train()

        self.change_tracks(iterations=iterations)

    def change_tracks(self, iterations):
        """
        Change the tracks.
        """
        for _ in range(self._railnet.get_max_trains()):
            self.change_one_track(iterations)

    def change_one_track(self, iterations):
        """
        Create for each trainroute multiple new
        trainroutes that could possibly replace it.
        """

        # quality of the railnet with the current train
        best_quality = self._railnet.quality()

        # remove the train
        removed_train = self._railnet.get_trains()[0]
        best_replacement = removed_train

        # calculate quality of the railnet without the current train
        self._railnet.remove_train(removed_train)
        removed_quality = self._railnet.quality()
        if removed_quality > best_quality:
            best_quality = removed_quality

        # create the trains that could possibly replace the original
        for _ in range(iterations):

            # create new train, calculate quality, then remove it
            self.run_one_train()
            new_quality = self._railnet.quality()
            new_train = self._railnet.get_trains()[-1]
            self._railnet.remove_train(new_train)

            # if the new train is better, replace it as the best train
            if new_quality > best_quality:
                best_quality = new_quality
                best_replacement = new_train

        # add the best train out of the lot to the railnet
        if best_quality > removed_quality:
            self._railnet.add_train(best_replacement)
