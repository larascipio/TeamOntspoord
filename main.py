"""
main.py
"""

# add the 'code' directory to the path to use functions from load.py
import os, sys
from re import I
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, 'code'))

from load import *
from bad_algorithm import *
from output import *
from change_connections import *
from simple_visualization import *
import matplotlib.pyplot as plt

def reset_model():
    for station in list(stationdictionary.values()):
        station._passed = False
    for connection in connectionlist:
        connection._passed = False

if __name__ == '__main__':
    file_stations = './data/StationsNationaal.csv'
    file_connections = './data/ConnectiesNationaal.csv'

    qualityroutes = {}
    load(file_stations, file_connections)

    #station_failure('Utrecht Centraal')

    for _ in range(100):
        quality, route = make_bad_routes(list(stationdictionary.values()), 20, 180)
        # TODO overwrite sommige dictionary entries
        qualityroutes[quality] = route
        reset_model()

    plt.hist(qualityroutes.keys(), color='g')
    plt.ylabel('Quality')
    plt.savefig('lijnvoeringkwaliteit.png')

    # the best route
    highest = max(qualityroutes)
    output(highest, qualityroutes[highest])
