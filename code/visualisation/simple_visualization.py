"""
simple_visualization.py

Mostly used by Tim, because his laptop can't handle plotly
Just gives a plot of all the used connections - not necessary for final product or solution
"""

import matplotlib.pyplot as plt
# from matplotlib.pyplot import cm
# import numpy as np

# def simple_visualization(stationdictionary, connectionlist, route):
#     """Visualizes all the tracks in a plot"""
#     plt.figure(figsize=(25, 35))

#     for station in list(stationdictionary.values()):
#         plt.plot(float(station._x), float(station._y), 'o', color='b')
#         plt.annotate(station._name, (float(station._x), float(station._y)))

#     for connection in connectionlist:
#         begin = [float(connection._stations[0]._x), float(connection._stations[1]._x)]
#         end = [float(connection._stations[0]._y), float(connection._stations[1]._y)]
#         plt.plot(begin, end, color='y')

#     i = 5.25
#     for train in route:
#         x_routes = []
#         y_routes = []
#         for station in train.get_stations():
#             station_x, station_y = station.get_position()
#             x_routes.append(station_x)
#             y_routes.append(station_y)
#         color = iter(cm.rainbow(np.linspace(0, 1, len(route))))
#         c = next(color)
#         plt.plot(x_routes, y_routes, linewidth=i, c=c)
#         i -= 0.25

#     plt.title('Railway map of the Netherlands')
#     plt.savefig('railway_map.png')



def simple_visualization(railnet):
    """Visualizes all the tracks in a plot"""
    plt.figure(figsize=(25, 35))

    for station in railnet.get_stations():
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