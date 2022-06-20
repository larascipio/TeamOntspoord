import random
<<<<<<< HEAD
from all_code.algorithms.random_algorithm import Make_Random_Routes
from all_code.classes.train import Train
=======
from .random_algorithm import Make_Random_Routes
from code.classes.train import Train
>>>>>>> 97cd6a500997dc46a034fbaca08233dbfd6c8633
import random

class Make_Greedy_Routes(Make_Random_Routes):
    """
    A more greedy random algorithm that creates connections based on randomness and heuristics.
    Almost all of the functions are eqal to those of the Make_Random_Routes class, which is why
    we use that as a parent class.
    """

    def change_amount_of_trains(self, self._max_trains):


# Less random amount of trains 
    def run(self):
        """
        Run the algorithm.
        """
        # Create a random amount of trains within the constraint (BIAS: 0 = eruit )
        for _ in range(self._amount_of_trains):
            # create a train
            train = self.create_train()

            if not train:
                return

        # Keep going until the route is 2 hours
            while train.is_running():
                connection = train.choose_random_connection()

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