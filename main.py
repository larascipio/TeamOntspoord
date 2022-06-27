"""
main.py

Programmeertheorie - minor programmeren
Lara, Tim, Eva

- Can be used to run any of the algorithms created for the RailNL case.
- Uses command line arguments for choosing the dataset, the algorithm and 
    how the algorithm should be used.
"""

# ------------------------------- Imports --------------------------------------

from code.algorithms.bad_algorithm import Make_Greedy_Routes
from code.algorithms.random_algorithm import Make_Random_Routes
from code.algorithms.simulated_annealing import Hillclimber, Simulated_Annealing
from code.algorithms.simulated_annealing import Reheating
from code.algorithms.random_iteration import Make_Iterated_Routes
from code.algorithms.biased_iteration import Make_Biased_Routes
from code.algorithms.depth_first import Depth_First

from code.visualisation.plotly_animation import create_animation
from code.visualisation.plotly_live import Live_Plot
from code.visualisation.output import output
from code.visualisation.quality_hist import quality_hist
# from code.visualisation.simple_visualization import simple_visualization

from code.classes.structure import Railnet

import pandas as pd
import argparse

if __name__ == '__main__':

    # --------------------------- Read command line ----------------------------

    parser = argparse.ArgumentParser(
        description='Use different algorithms to find solutions for the RailNL case.')
    parser.add_argument(
        "type", 
        choices=['holland','national'],
        help="Choose between the dataset for hollands or national railways."
        )
    subparsers = parser.add_subparsers(dest='subparser_name')

    subparser_algorithm = subparsers.add_parser(
        'algorithm',
        help='Run a specific algorithm.'
    )
    subparser_algorithm.add_argument(
        "algorithm", 
        choices=[
            'random',
            'greedy',
            'hillclimber',
            'annealing',
            'reheating',
            'random_iteration',
            'biased_iteration',
            'depth_first'
        ],
        default='random',
        help="Choose what algorithm you would like to run."
        )
    subparser_algorithm.add_argument(
        "make",
        choices=['once', 'hist', 'best'],
        help="Choose what you would like to see from the chosen algorithm."
    )

    subparsers_experiment = subparsers.add_parser(
        'experiment',
        help='Perform an experiment on all agorithms.'
    )
    subparsers_experiment.add_argument(
        'runs', 
        default=1, 
        type=int,
        help='Provide the number of runs to perform for each algorithm.'
    )

    args = parser.parse_args()

    if not args.subparser_name:
        parser.print_help()

    # --------------------------- Load in rails --------------------------------

    if args.type == 'holland':
        file_stations = 'data/StationsHolland.csv'
        file_connections = 'data/ConnectiesHolland.csv'
        max_trains = 7
        max_time = 120
    else:
        file_stations = 'data/StationsNationaal.csv'
        file_connections = 'data/ConnectiesNationaal.csv'
        max_trains = 20
        max_time = 180

    rails = Railnet(max_trains, max_time)
    rails.load(file_stations, file_connections)

    # --------------------------- Choose algorithm -----------------------------
    
    if args.subparser_name == 'algorithm':

        if args.algorithm == 'random':
            Algorithm = Make_Random_Routes
        elif args.algorithm == 'greedy':
            Algorithm = Make_Greedy_Routes
        elif args.algorithm == 'hillclimber':
            Algorithm = Hillclimber
        elif args.algorithm == 'annealing':
            Algorithm = Simulated_Annealing
        elif args.algorithm == 'reheating':
            Algorithm = Reheating
        elif args.algorithm == 'random_iteration':
            Algorithm = Make_Iterated_Routes
        elif args.algorithm == 'biased_iteration':
            Algorithm = Make_Biased_Routes
        elif args.algorithm == 'depth_first':
            Algorithm = Depth_First

    # --------------------------- Run once -------------------------------------

        if args.make == 'once':

            route = Algorithm(rails)
            route.run()
            route_quality = rails.quality()

            print(route_quality)
            output(route_quality, rails.get_trains(), './code/output/output.csv')
            create_animation(rails)

    # --------------------------- Create histogram -----------------------------

        elif args.make == 'hist':
            qualities = []
            for i in range(100):

                # run the algorithm multiple times
                print(i)
                rails.reset()
                route = Algorithm(rails)
                route.run()
                qualities.append(rails.quality())

            # Create hist for the qualities of all runs 
            quality_hist(qualities)
    
    # --------------------------- Find best value ------------------------------

        elif args.make == 'best':
            best_qual = 0
            best_route = None
            # plot = Live_Plot(rails)
            
            for _ in range(10000):

                # run the algorithm multiple times
                rails.reset()
                route = Algorithm(rails)
                route.run()

                # show and save the best run till now
                if rails.quality() >= best_qual:
                    best_qual = rails.quality()
                    best_route = rails.get_trains()
                    print(best_qual)
                    output(best_qual,rails.get_trains(),'./code/output/output.csv')
                    create_animation(rails)

            # # show the best route again
            # print(best_route)
            # print(best_qual)
            # output(best_qual,best_route,'./code/output/output.csv')
            # rails.reset()
            # rails.restore_routes(best_route)
            # create_animation(rails)

    # --------------------------- Perform experiment ---------------------------

    elif args.subparser_name == 'experiment':
        algorithms = [
            Make_Random_Routes, 
            Make_Greedy_Routes, 
            Hillclimber, 
            Simulated_Annealing,
            Reheating,
            Make_Iterated_Routes,
            Make_Biased_Routes,
            Depth_First
        ]
        
        df = pd.DataFrame(columns=[a.__name__ for a in algorithms], index = [i for i in range(args.runs)])
        print(df)

        for Algorithm in algorithms:
            for i in range(args.runs):
                rails.reset()
                route = Algorithm(rails)
                route.run()
                df.loc[Algorithm.__name__, i] = rails.quality()
            # run iterations
            # save in dataframe
            print(Algorithm.__name__)
        
        # print(df)
    
    else:
        parser.print_help()

    