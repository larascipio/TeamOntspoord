import plotly.graph_objects as go
from load import *
from bad_algorithm import *

file_stations = '../data/StationsNationaal.csv'
file_connections = '../data/ConnectiesNationaal.csv'
stationsdict = load(file_stations, file_connections)
stations = list(stationsdict.values())

# create the connections
data = []
distances = []
for connection in connectionlist:
    x = []
    y = []
    for station in connection._stations:
        x.append(station._x)
        y.append(station._y)
    data.append(go.Scatter(x=x,y=y, marker=dict(color='blue', size=5), hoverinfo='skip'))

    distances.append(connection._distance)

print(sum(distances) / len(distances))

# create the scatter and lines for the map
x = []
y = []
name = []
for station in stations:
    x.append(station._x)
    y.append(station._y)
    name.append(station._name)
# print(x, y)
data.append(go.Scatter(x=x, y=y, mode='markers', hovertext=name, hoverinfo='text'))

# create the frames
quality, route = make_bad_routes(stations, 20, 180, 89)
train = route[0]
x_frames = []
y_frames = []
for station in train._stations_traveled:
    x_frames.append(station._x)
    y_frames.append(station._y)
frames = [go.Frame(
    data=[go.Scatter(
        x=[x_frames[k]],
        y=[y_frames[k]],
        mode='markers',
        marker=dict(color='yellow', size=20)
    )])
    for k in range(len(x_frames))]

# make the figure
fig = go.Figure(
    data=data,
    layout=go.Layout(
        xaxis=dict(range=[min(x)-0.1, max(x)+0.1], autorange=False),
        yaxis=dict(range=[min(y)-0.2, max(y)+0.2], autorange=False),
        title_text='A map of all trainstations and connections', 
        hovermode='closest', #TODO hovermode verwijder coordinaten
        updatemenus=[dict(
            type='buttons',
            buttons=[dict(
                label='Play',
                method='animate',
                args=[None]
            )])]
    ),
    frames=frames
)

fig.show()