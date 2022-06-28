# from code.visualisation.plotly_animation import create_gif
# create_gif('hillclimber')

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
from code.algorithms.simulated_annealing import Hillclimber, Simulated_Annealing, Reheating
from code.classes.structure import Railnet
from code.visualisation.plotly_animation import create_animation
from code.visualisation.plotly_live import Live_Plot
from code.visualisation.quality_hist import quality_hist
from code.visualisation.mean_plot import plot_analysis, simple_plot, plot_3d
from code.visualisation.output import output
import argparse
import statistics
import math
import pandas as pd

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

    rails = Railnet(max_trains, max_time)
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

    rails.reset()
    reheat = Reheating(rails)
    reheat.run()
    # print(reheat.best)
    # print(reheat.temps)
    # print(reheat.current)

    simple_plot(reheat.best, 'best', reheat.temps, 'temp', reheat.current, 'qual')

    # trains = rails.get_trains()
    # for train in trains:
    #     for connection in train.get_connections():
    #         print(connection)
    # print(len(trains))
    # print([train.get_distance() for train in trains])
    print(rails.quality())

    create_animation(rails)

    # ----------------------------- Create hist -------------------------------
    # hillclimber_qualities = []
    # for _ in range(1000):
    #     rails.reset()
    #     route = Hillclimber(rails, max_trains, max_time)
    #     route.run(iterations)
    #     route_quality = route.quality()
    #     hillclimber_qualities.append(route_quality)
        
    
    # # Create hist for best routes 
    # quality_hist(hillclimber_qualities)



    # annealing_qualities = []
    # for _ in range(1000):
    #     rails.reset()
    #     route = Simulated_Annealing(rails, max_trains, max_time, 1)
    #     route.run(iterations)
    #     route_quality = route.quality()
    #     annealing_qualities.append(route_quality)
        
    
    # # Create hist for best routes 
    # quality_hist(annealing_qualities)

    # ----------------------------- Different starting temps ------------------

    # # loop the starting temp from 0.000001 to 1,000,000
    # starting_temp = 1
    # avg = []
    # std = []
    # temps = []
    # multiplyby = math.sqrt(10)
    # while starting_temp < 10001:
    # # for starting_temp in range(10,101,5):
    #     print(starting_temp)
    #     qual = []

    #     # run the algorithm 50 times
    #     for _ in range(50):
    #         rails.reset()
    #         annealing = Reheating(rails, start_temp=starting_temp)
    #         annealing.run(10000)
    #         qual.append(rails.quality())
    #         # simple_plot(annealing.temps)
        
    #     avg.append(statistics.mean(qual))
    #     std.append(statistics.stdev(qual))
    #     temps.append(starting_temp)

    #     starting_temp *= multiplyby

    # # temps = [0.001, 0.0031622776601683794, 0.01, 0.0316227766016838, 0.10000000000000002, 0.316227766016838, 1.0000000000000002, 3.1622776601683804, 10.000000000000004, 31.622776601683807, 100.00000000000004, 316.2277660168381, 1000.0000000000005, 3162.277660168381, 10000.000000000005, 31622.776601683814, 100000.00000000007, 316227.7660168382, 1000000.0000000009]
    # # avg = [5600.1089887640455, 5572.604269662922, 5613.6865168539325, 5624.519550561798, 5637.236853932584, 5558.061797752809, 5716.514157303371, 5696.950112359551, 5652.495280898876, 5705.349438202247, 5680.943820224719, 5686.646067415731, 5631.051235955057, 5626.905842696629, 5606.821123595506, 5589.224719101124, 5588.0220224719105, 5551.205617977528, 5645.897078651686]
    # # std = [342.405865938405, 265.70818364630253, 357.22017807297266, 359.29602254411327, 309.65545877874973, 361.113566739956, 310.0048210530058, 364.78651992743886, 325.84433079507033, 328.863989441605, 290.8834433296652, 327.11292413528014, 270.8930068139508, 312.8558454032602, 321.1682575062204, 329.1621050196368, 376.83159235786854, 350.78753128378366, 320.6070156185937]

    # print(avg)
    # print(std)

    # plot_analysis(
    #     temps=temps, 
    #     mean=avg, 
    #     std=std, 
    #     colors=(151, 127, 215), 
    #     name=f'average quality at {iterations} iterations', 
    #     xaxis='starting temperature',
    #     yaxis='quality',
    #     title='The quality for different starting temperatures'
    # )

    # ----------------------------- number of iterations ----------------------

    # # loop the number of iterations from 100 to 1,000,000
    # iterations = 1
    # avg = []
    # std = []
    # temps = []
    # while iterations < 100001:
    # # for iterations in range(1, 100001, 1):
    #     qual = []
    #     print(iterations)

    #     # run the algorithm 50 times
    #     for _ in range(50):
    #         rails.reset()
    #         annealing = Simulated_Annealing(rails, max_trains, max_time, start_temp=20)
    #         annealing.run(iterations)
    #         qual.append(annealing.quality())
        
    #     avg.append(statistics.mean(qual))
    #     std.append(statistics.stdev(qual))
    #     temps.append(iterations)

    #     iterations *= 10

        
    # print(avg)
    # print(std)

    # plot_analysis(
    #     temps=temps, 
    #     mean=avg, 
    #     std=std, 
    #     colors=(151, 127, 215), 
    #     name='average quality for a linear starting temperature of 20', 
    #     xaxis='number of iterations',
    #     yaxis='quality',
    #     title='Analysis of the number of iterations'
    # )

    # ----------------------------- Base --------------------------------------

    # # loop the number of iterations from 100 to 1,000,000
    # # base = 0.1
    # avg = []
    # std = []
    # temps = []
    # # while base < 1:
    # for base in range(9980,9990,1):
    #     base /= 10000
    #     qual = []
    #     print(base)

    #     # run the algorithm 50 times
    #     for _ in range(50):
    #         rails.reset()
    #         annealing = Reheating(rails, base=base)
    #         annealing.run(10000)
    #         qual.append(rails.quality())
        
    #     avg.append(statistics.mean(qual))
    #     std.append(statistics.stdev(qual))
    #     temps.append(base)

    #     # iterations *= 10

        
    # print(avg)
    # print(std)

    # plot_analysis(
    #     temps=temps, 
    #     mean=avg, 
    #     std=std, 
    #     colors=(151, 127, 215), 
    #     name='average quality for a linear starting temperature of 20', 
    #     xaxis='base',
    #     yaxis='quality',
    #     title='Analysis of the base'
    # )

    " ----------------------------- temp and base ----------------------------- "

    # # loop the starting temp from 0.000001 to 1,000,000
    # df = pd.DataFrame(columns = ['result', 'temp', 'base'])
    # # avg = []
    # # std = []
    # # temps = []

    # starting_temp = 1
    # # multiplyby = math.sqrt(10)
    # while starting_temp < 100001:
    # # for starting_temp in range(10,101,5):
    #     print(starting_temp)
    #     for base in range(995,1000,1):
    #         base /= 1000

    #         qual = []

    #         # run the algorithm 50 times
    #         for _ in range(10):
    #             rails.reset()
    #             annealing = Simulated_Annealing(rails, start_temp=starting_temp, base=base)
    #             annealing.run(10000)
    #             qual.append(rails.quality())
            
    #         df = pd.concat([df,pd.DataFrame({'result':statistics.mean(qual),'temp':starting_temp,'base':base}, index=[0], columns=['result', 'temp', 'base'])], ignore_index=True)

    #     starting_temp *= 10
    
    # print(df)
    # df.to_csv('temp_base.csv')
    # # df = pd.read_csv('temp_base.csv')
    # print(df)
    # plot_3d(df,'temp','base','result')

    # ----------------------------- Find best ---------------------------------
    
    # best_qual = 0
    # best_route = None
    # plot = Live_Plot(rails)
    
    # for _ in range(10000):
    #     rails.reset()
    #     route = Simulated_Annealing(rails, max_trains, max_time, 1)
    #     route.run(iterations)
    #     if route.quality() >= best_qual:
    #         best_qual = route.quality()
    #         best_route = route
    #         print(best_qual)
    #         plot.update_fig(best_route)
    #         output(best_qual, best_route.get_trains(), './code/output/output.csv')

    # print(best_route)
    # print(best_qual)
    # output(best_qual, best_route.get_trains(), './code/output/output.csv')
    # create_animation(rails, best_route)


    # display = Run_Algorithms_Live(Simulated_Annealing, rails, iterations, max_trains, max_time)