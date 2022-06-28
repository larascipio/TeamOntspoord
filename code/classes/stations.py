"""
stations.py

Programmeertheorie - minor programmeren
Lara, Tim, Eva

- Houses the classes for the stations and the connections.
"""

# ------------------------------- Station --------------------------------------

class Station():
    def __init__(self, station: str, x_coordinate: float, y_coordinate: float):
        """Create a station at the given coordinates."""
        self._connections = {}
        self._name = station
        self._x = float(y_coordinate)
        self._y = float(x_coordinate)
        self._passed = False

    def get_connections(self):
        return list(self._connections.values())

    def get_position(self):
        return (self._x, self._y)

    def get_name(self):
        return self._name

    def add_connection(self, connection) -> None:
        """Add a connection from this station to the next."""
        station = connection.get_destination(self)
        self._connections[station.get_name()] = connection

    def remove_connection(self, connection):
        """
        Removes a connection from this station.
        Used by 
        """
        station = connection.get_destination(self)
        self._connections.pop(station.get_name())

    def get_connection_by_station(self, station_name: str):
        """
        Returns the connections that belongs to this station.
        Used by Railnet.restore_routes.
        """
        if not station_name in self._connections:
            return None
        return self._connections[station_name]

    def travel(self):
        self._passed = True
    
    def passed(self):
        return self._passed

    def reset(self):
        self._passed = False

    def print_info(self):
        """Print the information of this station."""
        print(self._name)
        print('Connections:')
        for connection in self._connections:
            print(connection.get_destination(self)._name)
        print(f'Location: ({self._x}, {self._y})')
        print()

    def __repr__(self):
        return f'Station {self._name}'

# ------------------------------- Connections ----------------------------------

class Connection():
    def __init__(self, station1, station2, distance: int):
        """Create a connection between station1 and station2."""
        self._stations = (station1, station2)
        self._distance = int(distance)
        self._passed = 0

    def get_destination(self, station):
        """Return the destination from travelling this connection."""
        if station == self._stations[0]:
            return self._stations[1]
        return self._stations[0]

    def get_stations(self):
        return self._stations

    def travel(self):
        self._passed += 1

    def passed(self):
        if self._passed > 0:
            return True
        return False
    
    def remove(self):
        if self._passed > 0:
            self._passed -= 1
        else:
            raise Exception('You cannot remove this connection, as it is not passed.')
        
    def reset(self):
        self._passed = 0

    def get_distance(self) -> int:
        return self._distance

    def get_times_passed(self) -> int:
        return self._passed

    def __repr__(self):
        return f'Connection {self._stations[0].get_name()}-{self._stations[1].get_name()}'
