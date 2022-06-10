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
import matplotlib.pyplot as plt

if __name__ == '__main__':
    file_stations = './data/StationsNationaal.csv'
    file_connections = './data/ConnectiesNationaal.csv'

    qualityroutes = {}
    x_values = []

    for _ in range(100):
        load(file_stations, file_connections)
        #station_failure('Utrecht Centraal')
        quality, route = make_bad_routes(list(stationdictionary.values()), 20, 180)
        # TODO overwrite sommige dictionary entries
        qualityroutes[quality] = route

    # TODO maak elegantere x-as voor tabel, zonder dubbele loop
    for i in range(len(qualityroutes)):
        x_values.append(i)

    plt.ylim(min(qualityroutes), max(qualityroutes))
    plt.bar(x_values, qualityroutes.keys(), color='g')
    plt.ylabel('Quality')
    #plt.xticks(rotation=90)
    plt.savefig('lijnvoeringkwaliteit.png')
    # the best route
    highest = max(qualityroutes)
    output(highest, qualityroutes[highest])
