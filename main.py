"""
main.py
"""
import os, sys
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, 'code'))

# import the used programs
import load

def main():
    """Use one of the algorithms to find the best trainroutes."""
    file_stations = './data/StationsHolland.csv'
    file_locations = './data/ConnectiesHolland.csv'
    load()

if __name__ == '__main__':
    main()