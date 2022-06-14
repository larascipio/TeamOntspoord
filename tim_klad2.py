from load import *
import matplotlib.pyplot as plt
import random

def simple_visualization():
    """Visualizes all the tracks in a plot"""
    # TODO pas grootte aan aan de hand van soort kaart
    plt.figure(figsize=(25, 35))

    for station in list(stationdictionary.values()):
        plt.plot(float(station._x), float(station._y), 'o', color='b')
        plt.annotate(station._name, (float(station._x), float(station._y)))

    for connection in connectionlist:
        begin = [float(connection._stations[0]._x), float(connection._stations[1]._x)]
        end = [float(connection._stations[0]._y), float(connection._stations[1]._y)]
        if connection._passed is True:
            plt.plot(begin, end, color='y')
        else:
            plt.plot(begin, end, color='b')

    plt.title('Railway map of the Netherlands')
    plt.savefig('railway_map.png')

# TODO nog niet getest!
def follow_track(route):
    """Follow a track again"""
    for train in route:
        track = route[train]
        stationdictionary[track[i]].travel()
        for i in range(len(track) - 1):
            for connection in stationdictionary[track[i]]._connections:
                if connection.get_destination() == track[i + 1]:
                    connection.travel()
            stationdictionary[track[i + 1]].travel()

# TODO Sla connections die gepassed zijn ergens op


def weighted_routes():
    end_stations = []
    weighted_chance = []
    other_end_stations = []
    # TODO Start-station weighted chance - miss ook weighted chance for de andere
    for station in list(stationdictionary.values()):
        if len(station._connections) < 2: # TODO nog veranderen in stations.py, misschien de hoeveelheid connecties in int opslaan?
            end_stations.append(station)
        else:
            weighted_chance.append(len(station._connections))
            other_end_stations.append(station._name)

    
    for station in list(stationdictionary.values()):
        weighted_chance.append(len(station._connections))

    weighted_chance_start = [1 / x for x in weighted_chance]


if __name__ == "__main__":
    poo = set()
    pee = 100
    poo.add(pee)
    print(poo)



