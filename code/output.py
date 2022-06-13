import csv

def output(quality, trains):
    """Put output in a csv file called output.csv"""
    with open('output.csv', 'w', newline='') as file:

        writer = csv.writer(file)
        writer.writerow(["train", "stations"])
        x = 1
        for train in trains:
            writer.writerow([f"train_{x}", f"[{str(i) + ',' for i in train._route}]"])
            x += 1
        writer.writerow(["score", quality])