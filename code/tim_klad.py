import pandas as pd
import csv

def main():
    # GEBRUIK DICTREADER, LOADER.PY
    # COMMIT PULL PUSH

    # Create the Data Frame from the csv file, and sort by year and rating
    connection_dataFrame = pd.read_csv("data/ConnectiesHolland.csv")
    stations_dataFrame = pd.read_csv("data/StationsHolland.csv")
    print(connection_dataFrame)
    print(stations_dataFrame)

    with open("data/StationsHolland.csv", newline = '') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader: 
            print(row['station'], (row['x'], row['y']))
            #class initialise
            #

    with open("data/ConnectiesHolland.csv", newline = '') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader: 
            new_tuple = (row['station1'], row['station2'])
            
            print((row['station1'], (row['station2']), row['distance'])) 
            new_tuple = (row['station1'], row['station2'])
            print(new_tuple)



if __name__ == "__main__":
    main()

