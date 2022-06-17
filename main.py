"""
main.py
"""
from code.algorithms.bad_algorithm import Make_Bad_Routes
from code.algorithms.random_algorithm import Make_Random_Routes
from code.visualisation.plotly_animation import create_animation
from code.classes.structure import Railnet
from code.visualisation.quality_hist import quality_hist
# from code.visualisation.simple_visualization import simple_visualization
import argparse

if __name__ == '__main__':

    # use commandline arguments to choose the railroad
    parser = argparse.ArgumentParser(description='create routes')
    parser.add_argument(
        "type", 
        choices=['holland','national'],
        help="Use the holland or national railroads"
        )
    parser.add_argument(
        "algorithm", 
        choices=['random','bad'], 
        default='random', 
        help="The algorithm that will be used."
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

    # ----------------------------- Load in rails -----------------------------

    rails = Railnet()
    rails.load(file_stations, file_connections)

    # ----------------------------- Run once ----------------------------------
    if args.algorithm == 'bad':

        random_qualities = []
        for _ in range(1):
            rails.reset()
            route = Make_Bad_Routes(rails, max_trains, max_time)
            route.run()
            route_quality = route.quality()
            random_qualities.append(route_quality)
            
        
        # Create hist for best routes 
        quality_hist(random_qualities)

        # route = Make_Bad_Routes(rails, max_trains, max_time)
        # route.run()
        # quality = route.quality()

        # print(route)

        create_animation(rails, route)


    # rails.reset()
    # newroute = Make_Bad_Routes(rails, max_trains, max_time)
    # newroute.run()
    # print(newroute)  

    # ----------------------------- Create histogram of random ----------------

    elif args.algorithm == 'random':
        random_qualities = []
        for _ in range(1):
            rails.reset()
            route = Make_Random_Routes(rails, max_trains, max_time)
            route.run()
            route_quality = route.quality()
            random_qualities.append(route_quality)
            
        
        # Create hist for best routes 
        quality_hist(random_qualities)

        create_animation(rails, route)
