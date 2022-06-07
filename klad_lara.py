def load_station(filename):
    """Creates a graph of all room objects pointing to each other and returns a reference to the “first” room"""
    with open(filename) as f:
        for line in f:
            if line == "\n":
                break

            line = line.strip()
            list_line = line.split("\t")
            