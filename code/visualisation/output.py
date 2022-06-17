import csv

def output(quality: float, trains: list, outputfile: str):
    """Put output in a csv file called output.csv"""
    with open(outputfile, 'w', newline='') as file:

        writer = csv.writer(file)
        writer.writerow(["train", "stations"])
        x = 1
        for train in trains:
            route = '['
            for station in train._stations_traveled:
                route += station._name + ', '
            route = route[:-2]
            route += ']'
            writer.writerow([f"train_{x}", route])
            x += 1
        writer.writerow(["score", quality])