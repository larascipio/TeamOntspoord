from code.algorithms.random_algorithm import Make_Random_Routes

class Make_Iterated_Routes():

    def __init__(self, railnet):
        """
        Loads the railnet on which the algorithm will be used
        """
        self._railnet = railnet
        self._route = Make_Random_Routes(self._railnet) # Waarom gebruik je deze als je later zelf meer treinen toevoegd?
    
    def run(self):
        """
        Run the algorithm.
        """
        for _ in range(self._railnet.get_max_trains()):
            self._route.run_one_train()
        self.change_tracks(250)

    def change_tracks(self, iterations): # TODO comments! zo'n blok code is onleesbaar
        """
        Create for each train multiple new trains (using iterations) that could possibly replace it
        Replace the current train with the train that most positively affects the overall quality
        Or keep/remove the current train depending on what is best for the overall quality
        """

        for _ in range(self._railnet.get_max_trains()):
            start_quality = self._railnet.quality()

            removed_train = self._railnet.get_trains()[0]
            self._railnet.remove_train(removed_train)
            removed_quality = self._railnet.quality()

            if removed_quality > start_quality:
                best_quality = removed_quality
            else:
                best_quality = start_quality
                best_replacement = removed_train


            for _ in range(iterations):
                
                self._route.run_one_train()
                new_quality = self._railnet.quality()
                new_train = self._railnet.get_trains()[-1]
                self._railnet.remove_train(new_train)
                
                if new_quality > best_quality:
                    best_quality = new_quality
                    best_replacement = new_train

            if best_quality > removed_quality:
                self._railnet.add_train(best_replacement)

        # print(best_quality)
