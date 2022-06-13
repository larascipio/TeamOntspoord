"""
stations.py
"""

class Station():
    def __init__(self, station: str, x_coordinate: float, y_coordinate: float):
        """Create a station.s"""
        self._connections = []
        self._name = station
        self._x = float(y_coordinate)
        self._y = float(x_coordinate)
        # self._passed = False

    def add_connection(self, connection):
        """Add a connection from this station to the next."""
        self._connections.append(connection)

    # def travel(self):
    #     self._passed = True

    # def passed(self):
    #     return self._passed

    def get_connections(self):
        return self._connections

    def get_position(self):
        return (self._x, self._y)
    
    def get_name(self):
        return self._name

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

class Connection():
    def __init__(self, station1, station2, distance: int):
        """Create a connection between station1 and station2."""
        self._stations = (station1, station2)
        self._distance = int(distance)
        # self._passed = False

    def get_destination(self, station):
        """Return the destination from travelling this connection."""
        if station == self._stations[0]:
            return self._stations[1]
        return self._stations[0]

    # def travel(self):
    #     self._passed = True
    
    # def passed(self):
    #     return self._passed

    def get_distance(self):
        return self._distance

    def __repr__(self):
        return f'Connection {self._stations[0].get_name()}-{self._stations[1].get_name()}'