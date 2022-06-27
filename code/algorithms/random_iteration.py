from code.algorithms.random_algorithm import Make_Random_Routes

class Make_Iterated_Routes():

    def __init__(self, railnet):
        """
        Loads the railnet on which the algorithm will be used.
        """
        self._railnet = railnet

        # Use random algorithm to create trainroutes
        self._route = Make_Random_Routes(self._railnet)
    
    def run(self):
        """
        Run the algorithm.
        """
        for _ in range(self._railnet.get_max_trains()):
            self._route.run_one_train()
        self.change_tracks(1000)

    def change_tracks(self, iterations): 
        """
        Create for each trainroute multiple new 
        trainroutes that could possibly replace it.
        """

        for _ in range(self._railnet.get_max_trains()):
            # Quality of the railnet with the current train
            start_quality = self._railnet.quality()

            # Calculate quality of the railnet without the current train
            removed_train = self._railnet.get_trains()[0]
            self._railnet.remove_train(removed_train)
            removed_quality = self._railnet.quality()

            # If removing the train is preferable, save it as the best quality
            if removed_quality > start_quality:
                best_quality = removed_quality
            # Else, save the removed original train as the best quality 
            else:
                best_quality = start_quality
                best_replacement = removed_train

            # Create the trains that could possibly replace the original
            for _ in range(iterations):
                
                # Create new train, calculate quality, then remove it
                self._route.run_one_train()
                new_quality = self._railnet.quality()
                new_train = self._railnet.get_trains()[-1]
                self._railnet.remove_train(new_train)
                
                # If the new train is better, replace it as the best train
                if new_quality > best_quality:
                    best_quality = new_quality
                    best_replacement = new_train

            # Add the best train out of the lot to the railnet
            if best_quality > removed_quality:
                self._railnet.add_train(best_replacement)
