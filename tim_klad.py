import pandas as pd

def main():
    # GEBRUIK DICTREADER, LOADER.PY

    # Create the Data Frame from the csv file, and sort by year and rating
    connection_dataFrame = pd.read_csv("data/ConnectiesHolland.csv")
    stations_dataFrame = pd.read_csv("data/StationsHolland.csv")
    print(connection_dataFrame)
    print(stations_dataFrame)

if __name__ == "__main__":
    main()

