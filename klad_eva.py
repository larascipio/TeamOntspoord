# # state space?
# c = 3 # num_connections per station
# s = 61 # num_stations
# m = 10 # max connections per trein
# sum = 0
# for i in range(1,m):
#     # print(sum)
#     # print(pow(c,i)*s/2)
#     sum += pow(c,i)*s
# print('{:e}'.format(sum))
# from code.algorithms.bad_algorithm import make_bad_routes
from all_code.algorithms.simulated_annealing import Hillclimber, Simulated_Annealing
from all_code.classes.structure import Railnet
from all_code.visualisation.plotly_animation import create_animation
from all_code.visualisation.plotly_live import Run_Algorithms_Live, Live_Plot
from all_code.visualisation.quality_hist import quality_hist
from all_code.visualisation.mean_plot import plot_analysis
from all_code.visualisation.output import output
import argparse
import statistics

if __name__ == '__main__':
    # use commandline arguments to choose the railroad
    parser = argparse.ArgumentParser(description='create routes')
    parser.add_argument(
        "type", 
        choices=['holland','national'], 
        help="Use the holland or national railroads"
    )
    args = parser.parse_args()

    if args.type == 'holland':
        file_stations = './data/StationsHolland.csv'
        file_connections = './data/ConnectiesHolland.csv'
        max_trains = 7
        max_time = 120
        iterations = 10000
    else:
        file_stations = './data/StationsNationaal.csv'
        file_connections = './data/ConnectiesNationaal.csv'
        max_trains = 20
        max_time = 180
        iterations = 10000

    # ----------------------------- Initialize rails --------------------------

    rails = Railnet()
    rails.load(file_stations, file_connections)

    # ----------------------------- Run once ----------------------------------
    
    # algorithm = Hillclimber(rails, max_trains, max_time)
    # algorithm.run(iterations)

    # trains = algorithm.get_trains()
    # for train in trains:
    #     for connection in train.get_connections():
    #         print(connection)
    # print(len(trains))
    # print([train.get_distance() for train in trains])
    # create_animation(rails, algorithm)


    # rails.reset()
    # annealing = Simulated_Annealing(rails, max_trains, max_time, 10000)
    # annealing.run(iterations)

    # trains = annealing.get_trains()
    # for train in trains:
    #     for connection in train.get_connections():
    #         print(connection)
    # print(len(trains))
    # print([train.get_distance() for train in trains])


    # create_animation(rails, annealing, True)

    # ----------------------------- Create hist -------------------------------
    # hillclimber_qualities = []
    # for _ in range(100):
    #     rails.reset()
    #     route = Hillclimber(rails, max_trains, max_time)
    #     route.run(iterations)
    #     route_quality = route.quality()
    #     hillclimber_qualities.append(route_quality)
        
    
    # # Create hist for best routes 
    # quality_hist(hillclimber_qualities)



    # annealing_qualities = []
    # for _ in range(100):
    #     rails.reset()
    #     route = Simulated_Annealing(rails, max_trains, max_time, 1)
    #     route.run(iterations)
    #     route_quality = route.quality()
    #     annealing_qualities.append(route_quality)
        
    
    # # Create hist for best routes 
    # quality_hist(annealing_qualities)

    # ----------------------------- Different starting temps ------------------

    # # loop the starting temp from 0.000001 to 1,000,000
    # starting_temp = 0.0001
    # avg = []
    # std = []
    # temps = []
    # while starting_temp < 100:
    #     qual = []

    #     # run the algorithm 50 times
    #     for _ in range(50):
    #         rails.reset()
    #         annealing = Simulated_Annealing(rails, max_trains, max_time, starting_temp)
    #         annealing.run(iterations)
    #         qual.append(annealing.quality())
        
    #     avg.append(statistics.mean(qual))
    #     std.append(statistics.stdev(qual))
    #     temps.append(starting_temp)

    #     starting_temp *= 2

        
    # print(avg)
    # print(std)

    # plot_analysis(temps, avg, std, (151, 127, 215), 'linear temps')

    # ----------------------------- number of iterations ----------------------

    # # loop the number of iterations from 100 to 1,000,000
    # iterations = 100
    # avg = []
    # std = []
    # temps = []
    # for iterations in range(10000, 100001, 10000):
    #     qual = []

    #     # run the algorithm 50 times
    #     for _ in range(50):
    #         rails.reset()
    #         annealing = Simulated_Annealing(rails, max_trains, max_time, start_temp=1)
    #         annealing.run(iterations)
    #         qual.append(annealing.quality())
        
    #     avg.append(statistics.mean(qual))
    #     std.append(statistics.stdev(qual))
    #     temps.append(iterations)

    #     iterations *= 10

        
    # print(avg)
    # print(std)

    # plot_analysis(temps, avg, std, (151, 127, 215), 'number of iterations')

    # ----------------------------- Find best ---------------------------------
    
    best_qual = 0
    best_route = None
    plot = Live_Plot(rails)
    
    for _ in range(10000):
        rails.reset()
        route = Simulated_Annealing(rails, max_trains, max_time, 1)
        route.run(iterations)
        if route.quality() >= best_qual:
            best_qual = route.quality()
            best_route = route
            print(best_qual)
            plot.update_fig(best_route)

    print(best_qual)
    output(best_qual, best_route.get_trains(), './code/output/output.csv')
    # create_animation(rails, best_route)


    # display = Run_Algorithms_Live(Simulated_Annealing, rails, iterations, max_trains, max_time)