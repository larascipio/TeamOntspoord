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
stationlist = list(rails.get_stations().values())
minus_distance = 0
quality_difference_dict = {}


for station in stationlist:
    for connection in station.get_connections():
        minus_distance += connection.get_distance()

    total_distance = 1551 - minus_distance
    minus_trains = (total_distance // max_time + 1) * 100
    theoretical_quality = 10000 - minus_trains - total_distance
    quality_difference_dict[station.get_name()] = theoretical_quality
    minus_distance = 0

print(quality_difference_dict)

    
#     rails.reset
#     rails.load(file_stations, file_connections)



