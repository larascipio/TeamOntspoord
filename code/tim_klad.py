from load import *
import matplotlib.pyplot as plt

def visualize_tracks():
    """Visualizes all the tracks in a plot"""
    file_stations = '../data/StationsHolland.csv'
    file_connections = '../data/ConnectiesHolland.csv'
    load(file_stations, file_connections)
    actualagents = list(stationdictionary.values())

    plt.figure(figsize=(12, 25))

    for station in actualagents:
        plt.plot(float(station._y), float(station._x), 'o')
        plt.annotate(station._name, (float(station._y), float(station._x)))

    for connection in connectionlist:
        begin = [float(connection._stations[0]._y), float(connection._stations[1]._y)]
        end = [float(connection._stations[0]._x), float(connection._stations[1]._x)]
        plt.plot(begin, end, color='g')

    plt.title('Stations')
    plt.savefig('station.png')

if __name__ == "__main__":
    visualize_tracks()




