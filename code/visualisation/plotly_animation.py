import plotly.graph_objects as go
import plotly.express as px
import random

def create_animation(railnet, routeclass):

    # get the stations and connections
    stations = list(railnet.get_stations().values())
    connectionlist = list(railnet.get_connections().values())

    # create the colours for the trains
    route = routeclass.get_trains()
    num_trains = len(route)
    colorlist = px.colors.qualitative.Plotly
    # color = random.choices(colorlist, k=num_trains)
    color = colorlist + colorlist

    # add the first stations for every train to the data (weird animation thing plotly)
    first_x = []
    first_y = []
    for train in route:
        first_station = train._stations_traveled[0]
        first_x.append(first_station._x)
        first_y.append(first_station._y)
    data = [go.Scatter(
        x=first_x,
        y=first_y,
        # color = color,
        mode='markers',
        marker=dict(color=color, size=20),
        hoverinfo='skip'
    )]
    
    # train = route[0]
    # first_station = train._stations_traveled[0]
    # data = [go.Scatter(
    #     x=[first_station._x],
    #     y=[first_station._y],
    #     mode='markers',
    #     marker=dict(color='yellow', size=20),
    #     hoverinfo='skip'
    # )]

    # create the connections
    distances = []
    for connection in connectionlist:
        x = []
        y = []
        for station in connection._stations:
            x.append(station._x)
            y.append(station._y)
        data.append(go.Scatter(x=x,y=y, marker=dict(color='blue', size=1), hoverinfo='skip'))

        distances.append(connection._distance)

    # create the scatter and lines for the map
    x_stations = []
    y_stations = []
    name = []
    for station in stations:
        x_stations.append(station._x)
        y_stations.append(station._y)
        name.append(station._name)
    # print(x, y)
    data.append(go.Scatter(x=x_stations, y=y_stations, mode='markers', hovertext=name, hoverinfo='text'))

    # create the frames
    # quality, route = make_bad_routes(stations, 20, 180, 89)
    # train = route[0]
    x_frames = []
    y_frames = []
    # loop for the max length of a train = 30
    for pos in range(30):
        x = []
        y = []
        for train in route:
            train_length = len(train._stations_traveled)
            position = pos % (train_length * 2 - 1)
            if position >= train_length:
                position = train_length - (position % train_length + 2)
            x.append(train._stations_traveled[position]._x)
            y.append(train._stations_traveled[position]._y)

        x_frames.append(x)
        y_frames.append(y)
    frames = [go.Frame(
        data=[go.Scatter(
            x=x_frames[k],
            y=y_frames[k],
            # color = color,
            mode='markers',
            marker=dict(color=color, size=20),
            hoverinfo='skip'
        )])
        for k in range(len(x_frames))]

    # make the figure
    fig = go.Figure(
        data=data,
        layout=go.Layout(
            xaxis=dict(range=[min(x_stations)-0.1, max(x_stations)+0.1], autorange=False),
            yaxis=dict(range=[min(y_stations)-0.2, max(y_stations)+0.2], autorange=False),
            title_text='A map of all trainstations and connections', 
            hovermode='closest',
            updatemenus=[dict(
                type='buttons',
                buttons=[dict(
                    label='Play',
                    method='animate',
                    args=[None]
                )])],
            showlegend=False
        ),
        frames=frames
    )

    fig.show()