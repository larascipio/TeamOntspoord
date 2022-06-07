"""
stations.py


"""

class Station():
    def __init__(self, station: str, x_coordinate: float, y_coordinate: float):
        """Create a station.s"""
        self._connections = []
        self._name = station
        self._x = x_coordinate
        self._y = y_coordinate

    def add_connection(self, connection):
        """Add a connection from this station to the next."""
        self._connections.append(connection)

    def print_info(self):
        """Print the information of this station."""
        print(self._name)
        print('Connections:')
        for connection in self._connections:
            print(connection.get_destination(self)._name)
        print(f'Location: ({self._x}, {self._y})')
        print()

class Connection():
    def __init__(self, station1, station2, distance: int):
        """Create a connection between station1 and station2."""
        self._stations = (station1, station2)
        self._distance = distance

    def get_destination(self, station):
        """Return the destination from travelling this connection."""
        if station == self._stations[0]:
            return self._stations[1]
        return self._stations[0]
