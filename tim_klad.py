from code.classes.structure import Railnet
# from code.visualisation.quality_hist import quality_hist
from code.visualisation.output import output
from code.visualisation.simple_visualization import simple_visualization
# from code.visualisation.plotly_animation import create_animation
from tim_quality_hist import quality_hist
import argparse

file_stations = 'data/StationsNationaal.csv'
file_connections = 'data/ConnectiesNationaal.csv'
max_trains = 20
max_time = 180

# Loads the railnet
qualitydict = {}
rails = Railnet(max_trains, max_time)
rails.load(file_stations, file_connections)
stationlist = list(rails.get_stations().keys())

for station in stationlist:
    rails.station_failure(station)
    rails.get_max_quality()
    rails.reset
    rails.load(file_stations, file_connections)


# Failed station if desired


# Change a number of random connections of choice
for _ in range(args.changeconnection):
    rails.change_connection()


