"""
stations.py


"""

class Station():
    def __init__(self, station: str, x_coordinate: float, y_coordinate: float):
        self._connections = []
        self._name = station
        self._x = x_coordinate
        self._y = y_coordinate

    def add_connection(self, station: str, connection):
        """Add a connection from this station to the next."""
        self._connections.append(connection)

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