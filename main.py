"""
main.py
"""
from code.algorithms.bad_algorithm import Make_Bad_Routes
from code.algorithms.random_algorithm import Make_Random_Routes
from code.algorithms.simulated_annealing import Hillclimber, Simulated_Annealing
from code.visualisation.plotly_animation import create_animation
from code.visualisation.plotly_live import Live_Plot
from code.visualisation.output import output
from code.classes.structure import Railnet
from code.visualisation.quality_hist import quality_hist
# from code.visualisation.simple_visualization import simple_visualization
import argparse

if __name__ == '__main__':

    # ----------------------------- Read command line -------------------------

    parser = argparse.ArgumentParser(description='create routes')
    parser.add_argument(
        "type", 
        choices=['holland','national'],
        help="Use the holland or national railroads"
        )
    parser.add_argument(
        "algorithm", 
        choices=['random','bad','hillclimber','annealing'], 
        help="The algorithm that will be used."
        )
    parser.add_argument(
        "make",
        choices=['once', 'hist', 'best'],
        help="Choose what you would like to see from the chosen algorithm."
    )

    args = parser.parse_args()

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
    
    if args.algorithm == 'random':
        Algorithm = Make_Random_Routes
    elif args.algorithm == 'bad':
        Algorithm = Make_Bad_Routes
    elif args.algorithm == 'hillclimber':
        Algorithm = Hillclimber
    elif args.algorithm == 'annealing':
        Algorithm = Simulated_Annealing

    # ----------------------------- Load in rails -----------------------------

    rails = Railnet()
    rails.load(file_stations, file_connections)

    # ----------------------------- Run once ----------------------------------
    if args.make == 'once':

        route = Algorithm(rails, max_trains, max_time)
        route.run(100000)
        route_quality = route.quality()

        print(route)
        print(route_quality)
        output(route_quality, route.get_trains(), './code/output/output.csv')
        create_animation(rails, route)


    # ----------------------------- Create histogram --------------------------

    elif args.make == 'hist':
        qualities = []
        for _ in range(1000):
            rails.reset()
            route = Algorithm(rails, max_trains, max_time)
            route.run()
            qualities.append(route.quality())

        # Create hist for best routes 
        quality_hist(qualities)
    
    # ----------------------------- Find best value ---------------------------

    elif args.make == 'best':
        best_qual = 0
        best_route = None
        plot = Live_Plot(rails)
        
        for _ in range(10000):
            rails.reset()
            route = Algorithm(rails, max_trains, max_time)
            route.run()
            if route.quality() >= best_qual:
                best_qual = route.quality()
                best_route = route
                print(best_qual)
                plot.update_fig(best_route)
                output(best_qual, best_route.get_trains(), './code/output/output.csv')

        print(best_route)
        print(best_qual)
        output(best_qual, best_route.get_trains(), './code/output/output.csv')
        create_animation(rails, best_route)
