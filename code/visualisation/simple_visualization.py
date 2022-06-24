"""
simple_visualization.py

Mostly used by Tim, because his laptop can't handle plotly
Just gives a plot of all the used connections - not necessary for final product or solution
"""

import matplotlib.pyplot as plt

def simple_visualization(railnet):
    """Visualizes all the tracks in a plot"""
    plt.figure(figsize=(25, 35))

    for station in list(railnet.get_stations().values()):
        plt.plot(float(station._x), float(station._y), 'o', color='b')
        plt.annotate(station._name, (float(station._x), float(station._y)))

    for connection in railnet.get_connections():
        begin = [float(connection._stations[0]._x), float(connection._stations[1]._x)]
        end = [float(connection._stations[0]._y), float(connection._stations[1]._y)]
        if connection.passed() is True:
            plt.plot(begin, end, color='b')
        else:
            plt.plot(begin, end, color='y')

    plt.title('Railway map of the Netherlands')
    plt.savefig('railway_map.png')