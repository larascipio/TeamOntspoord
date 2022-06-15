"""
main.py
"""
# from code.classes.load import load
from code.algorithms.bad_algorithm import Make_Bad_Routes
from code.algorithms.random_algorithm import Make_Random_Routes
from code.visualisation.plotly_animation import create_animation
from code.classes.structure import Railnet
from code.visualisation.quality_hist import quality_hist
# from code.classes.change_connections import *
# from code.visualisation.simple_visualization import *
import argparse

if __name__ == '__main__':

    # use commandline arguments to choose the railroad
    parser = argparse.ArgumentParser(description='create routes')
    parser.add_argument("type", choices=['holland','national'], help="Use the holland or national railroads")
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


    # ----------------------------- Run once ----------------------------------
    rails = Railnet()
    rails.load(file_stations, file_connections)

    route = Make_Bad_Routes(rails, max_trains, max_time)
    route.run()
    quality = route.quality()

    print(route)

    create_animation(rails, route)


    # rails.reset()
    # newroute = Make_Bad_Routes(rails, max_trains, max_time)
    # newroute.run()
    # print(newroute)  

    # ----------------------------- Create histogram --------------------------

    # qualityroutes = {}
    # rails = Railnet()
    # rails.load(file_stations, file_connections)
    # for _ in range(100):
    #     route = Make_Bad_Routes(rails, max_trains, max_time) # TODO dit moet het random-algoritme worden
    #     route.run()
    #     qualityroutes[quality] = route
    #     rails.reset()
    
    # # Create hist for best routes 
    # quality_hist(qualityroutes)



