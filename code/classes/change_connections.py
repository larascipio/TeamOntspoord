from code.classes.load import load
import random

def station_failure(failed_station):
    """Removes a failed stations from the dictionary, including all connections to it"""
    for connection in stationdictionary[failed_station]._connections:
        connectionlist.remove(connection)
        for station in connection._stations:
            if station is not stationdictionary[failed_station]:
                station._connections.remove(connection)
    del stationdictionary[failed_station]

def remove_random_connections():
    """Removes three random connections - if a stations has no more connections, remove it too"""
    for i in range(3):
        removed_connection = random.choice(connectionlist)
        connectionlist.remove(removed_connection)
        for station in removed_connection._stations:
            station._connections.remove(removed_connection)
            if len(station._connections) == 0:
                del stationdictionary[station]

# TODO Deze code is nog niet af, werkt als het goed is wel
def change_random_connections():
    """Removes three random connections - replaces them with three new ones with at least one of stations"""
    possible_removal_list = []
    for i in range(3):
        changed_connection = random.choice(connectionlist)
        # TODO Hoe maak ik de distance correct, ivm de afstand
        new_distance = changed_connection._distance
        connectionlist.remove(changed_connection)
        for station in changed_connection._stations:
            station._connections.remove(changed_connection)
            possible_removal_list.append(station)
        new_start_station = random.choice(changed_connection._stations)
        new_end_station = random.choice(list(stationdictionary.values()))
        # TODO Zodat niet dezelfde verbinding terugkomt, hoe maak ik dit eleganter?
        while new_end_station in changed_connection._stations:
            new_end_station = random.choice(list(stationdictionary.values()))
        # Create new connections
        new_connection = Connection(new_start_station, new_end_station, new_distance)
        stationdictionary[new_start_station].add_connection(new_connection)
        stationdictionary[new_end_station].add_connection(new_connection)
        connectionlist.append(new_connection)
    # Remove stations without a connection
    for station in possible_removal_list:
        if len(station._connections) == 0:
            del stationdictionary[station]

# TODO in plaats van stations te verwijderen uit de dictionary, ergens anders code stoppen zodat station daar niet begint?
# Zou beter werken voor de visualiatie, dan heb je stations zonder verbindingen nog wel op de kaart




