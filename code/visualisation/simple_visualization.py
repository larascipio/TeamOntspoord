from load import *
import matplotlib.pyplot as plt

# TODO OUTDATED - werkt niet zonder de global variables stationdictionary en connectionlist

def simple_visualization(stationdictionary, connectionlist):
    """Visualizes all the tracks in a plot"""
    plt.figure(figsize=(25, 35))

    for station in list(stationdictionary.values()):
        if station.passed() is True:
            plt.plot(float(station._x), float(station._y), 'o', color='b')
        else:
            plt.plot(float(station._x), float(station._y), 'o', color='y')
        plt.annotate(station._name, (float(station._x), float(station._y)))

    for connection in connectionlist:
        begin = [float(connection._stations[0]._x), float(connection._stations[1]._x)]
        end = [float(connection._stations[0]._y), float(connection._stations[1]._y)]
        if connection.passed() is True:
            plt.plot(begin, end, color='b')
        else:
            plt.plot(begin, end, color='y')

    plt.title('Railway map of the Netherlands')
    plt.savefig('railway_map.png')

def follow_track(route, stationdictionary):
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

# Following two functions don't require the travel() function

def follow_track_better(route, stationdictionary):
    """Follow a track again"""
    visualization_connection_set = set()
    for track in route:
        for i in range(len(track._route) - 1):
            current_stop = stationdictionary[track._route[i]]
            next_stop = stationdictionary[track._route[i + 1]]
            for connection in current_stop._connections:
                if connection.get_destination(current_stop) == next_stop:
                    visualization_connection_set.add(connection)
                    break
    return visualization_connection_set

def simple_visualization_better(visualization_connection_set, stationdictionary, connectionlist):
    """Visualizes all the tracks in a plot"""
    plt.figure(figsize=(25, 35))

    for station in list(stationdictionary.values()):
        plt.plot(float(station._x), float(station._y), 'o', color='y')
        plt.annotate(station._name, (float(station._x), float(station._y)))

    for connection in connectionlist:
        begin = [float(connection._stations[0]._x), float(connection._stations[1]._x)]
        end = [float(connection._stations[0]._y), float(connection._stations[1]._y)]
        if connection in visualization_connection_set:
            plt.plot(begin, end, color='b')
        else:
            plt.plot(begin, end, color='y')

    plt.title('Railway map of the Netherlands')
    plt.savefig('new_railway_map.png')

    