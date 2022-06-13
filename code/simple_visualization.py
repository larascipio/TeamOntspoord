from load import *
import matplotlib.pyplot as plt

def simple_visualization():
    """Visualizes all the tracks in a plot"""
    plt.figure(figsize=(25, 35))

    for station in list(stationdictionary.values()):
        if station._passed is True:
            plt.plot(float(station._x), float(station._y), 'o', color='b')
        else:
            plt.plot(float(station._x), float(station._y), 'o', color='y')
        plt.annotate(station._name, (float(station._x), float(station._y)))

    for connection in connectionlist:
        begin = [float(connection._stations[0]._x), float(connection._stations[1]._x)]
        end = [float(connection._stations[0]._y), float(connection._stations[1]._y)]
        if connection._passed is True:
            plt.plot(begin, end, color='b')
        else:
            plt.plot(begin, end, color='y')

    plt.title('Railway map of the Netherlands')
    plt.savefig('railway_map.png')

def follow_track(route):
    """Follow a track again"""
    for track in route:
        for i in range(len(track._route) - 1):
            current_stop = stationdictionary[track._route[i]]
            current_stop.travel()
            next_stop = stationdictionary[track._route[i + 1]]
            for connection in current_stop._connections:
                if connection.get_destination(current_stop) == next_stop:
                    connection.travel()
                    break
        next_stop.travel()

    