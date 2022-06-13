"""
main.py
"""
from code.classes.load import load, print_stationdictionary
from code.algorithms.bad_algorithm import make_bad_routes
from code.visualisation.output import output
# from code.classes.change_connections import *
# from code.visualisation.simple_visualization import *
# import matplotlib.pyplot as plt

def reset_model(stationdictionary, connectionlist):
    for station in list(stationdictionary.values()):
        station._passed = False
    for connection in connectionlist:
        connection._passed = False

if __name__ == '__main__':
    file_stations = './data/StationsHolland.csv'
    file_connections = './data/ConnectiesHolland.csv'

    qualityroutes = {}
    stationdictionary, connectionlist = load(file_stations, file_connections)

    #station_failure('Utrecht Centraal')

    for _ in range(1):
        quality, route = make_bad_routes(list(stationdictionary.values()), 7, 120, 28)
        # TODO overwrite sommige dictionary entries
        qualityroutes[quality] = route
        # for connection in connectionlist:
        #     print(connection._passed)

        reset_model(stationdictionary, connectionlist)
        
    best_qual = max(qualityroutes.keys())
    best_route = qualityroutes[best_qual]
    
    # for train in best_route:
    #     print(train._route)
    
    outputfile = './output/output.csv'
    output(best_qual, best_route, outputfile)

    # plt.hist(qualityroutes.keys(), color='g')
    # plt.ylabel('Quality')
    # plt.savefig('lijnvoeringkwaliteit.png')

    # # the best route
    # highest = max(qualityroutes)
    # output(highest, qualityroutes[highest])
