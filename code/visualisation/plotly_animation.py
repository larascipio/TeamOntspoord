from venv import create
import plotly.graph_objects as go
import plotly.express as px
# import random
import dash
from dash import dcc
from dash import html

def create_animation(railnet, routeclass, live=False):

    # # ask if you want moving trains
    # if input('Do you want moving trains? (y/n) ') == 'y':
    #     moving = True
    # else:
    #     moving = False
    moving = False

    # get the stations and connections
    stations = list(railnet.get_stations().values())
    connectionlist = list(railnet.get_connections().values())

    # create the colours for the trains
    route = routeclass.get_trains()
    colorlist = px.colors.qualitative.Plotly
    # color = random.choices(colorlist, k=num_trains)
    color = colorlist + colorlist

    # ----------------------------- Create the start of the animation ---------

    if moving:
        first_x = []
        first_y = []
        for train in route:
            first_station = train._stations_traveled[0]
            first_x.append(first_station._x)
            first_y.append(first_station._y)

        data = [go.Scattermapbox(
            lon=first_x,
            lat=first_y,
            # color = color,
            mode='markers',
            marker=dict(color=color, size=20),
            hoverinfo='skip'
        )]
    else:
        data = []

    # ----------------------------- Create the connections --------------------
    distances = []
    for connection in connectionlist:
        x = []
        y = []
        for station in connection._stations:
            x.append(station._x)
            y.append(station._y)
        # data.append(go.Scatter(x=x,y=y, marker=dict(color='blue', size=1), hoverinfo='skip'))
        data.append(go.Scattermapbox(
            lon=x,
            lat=y, 
            mode = 'markers+lines', 
            marker=dict(color='black', size=1), 
            hoverinfo='skip'
        ))

        distances.append(connection._distance)

    # ----------------------------- Create the stations -----------------------
    x_stations = []
    y_stations = []
    name = []
    for station in stations:
        x_stations.append(station._x)
        y_stations.append(station._y)
        name.append(station._name)
    # print(x, y)
    # data.append(go.Scatter(x=x_stations, y=y_stations, mode='markers', hovertext=name, hoverinfo='text'))
    data.append(go.Scattermapbox(
        lon=x_stations, 
        lat=y_stations, 
        mode='markers', 
        hovertext=name, 
        hoverinfo='text'))

    # ----------------------------- Create moving trains ----------------------

    if moving:

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
                data=[go.Scattermapbox(
                lon=x_frames[k],
                lat=y_frames[k],
                # color = color,
                mode='markers',
                marker=dict(color=[color[i%len(color)] for i in range(len(x_frames))], size=20),
                hoverinfo='skip'
            )])
            for k in range(len(x_frames))]

    # ----------------------------- Create the lines --------------------------

    i = 0
    for train in route:
        x_routes = []
        y_routes = []
        for station in train.get_stations():
            station_x, station_y = station.get_position()
            x_routes.append(station_x)
            y_routes.append(station_y)

        data += [go.Scattermapbox(
            lon=x_routes,
            lat=y_routes,
            mode = 'markers+lines',
            marker=dict(color=color[i%len(color)]),
            hoverinfo='skip'
        )]
        i += 1

    # ----------------------------- Create the figure -------------------------
    if moving:
        # make the figure
        fig = go.Figure(
            data=data,
            layout=go.Layout(
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
    else:
        # make the figure
        fig = go.Figure(
            data=data,
            layout=go.Layout(
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
            )
        )

    # try to include a map
    fig.update_layout(
        margin = {'l':0,'t':0, 'b':0, 'r':0},
        mapbox = {
            'center': {'lon': 5.2, 'lat': 52.2},
            'style': 'open-street-map',
            'zoom': 7
        }
    )

    if not live:
        fig.show()
        return

    app = dash.Dash()
    app.layout = html.Div([
        dcc.Graph(figure=fig, style={'width': '90vh', 'height': '90vh'})
    ])

    app.run_server(debug=True, use_reloader=False)
