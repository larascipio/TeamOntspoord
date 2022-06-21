import random
from .random_algorithm import Make_Random_Routes
from code.classes.train import Train
import random

class Make_Greedy_Routes(Make_Random_Routes):
    """
    A more greedy random algorithm that creates connections based on randomness and heuristics.
    Almost all of the functions are equal to those of the Make_Random_Routes class, which is why
    we use that as a parent class.
    """

    def choose_path(self):
        pass

# Less random amount of trains 
    def run(self):
        """
        Run the algorithm.
        """
        # Create the input amount of trains 
        for _ in range(self._max_trains):
            # create a train
            train = self.create_train()

            if not train:
                return

        # Keep going until the route is 2 hours
            while train.is_running():
                connection = train.choose_shortest_connection()

                if not connection:
                    break

                if connection.get_distance() + train.get_distance() < self._max_dist:
                    train.move(connection)
                else:
                    train.stop()

        # Save the train
            self._trains.append(train)    

# Less connections (fractie veranderd)


# Less connections (amount of connections)

# Less or more time 