import plotly.graph_objects as go
import plotly.express as px

import glob
from PIL import Image

# import random
# import dash
# from dash import dcc
# from dash import html

def create_animation(railnet, save_as_png=False, num=0):

    # # ask if you want moving trains
    # if input('Do you want moving trains? (y/n) ') == 'y':
    #     moving = True
    # else:
    #     moving = False
    moving = False

    # get the stations and connections
    stations = list(railnet.get_stations().values())
    connectionlist = list(railnet.get_connections())

    # create the colours for the trains
    route = railnet.get_trains()

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
            marker=dict(color=train.get_color(), size=20),
            hoverinfo='skip'
        )]
    else:
        data = []

    # ----------------------------- Create the connections ---------------------

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
            marker=dict(color='lightgray', size=1), 
            hoverinfo='skip'
        ))

        distances.append(connection._distance)

    # ----------------------------- Create the stations ------------------------

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

    # ----------------------------- Create moving trains -----------------------

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
                marker=dict(color=['black' for i in range(len(x_frames))], size=20),
                hoverinfo='skip'
            )])
            for k in range(len(x_frames))]

    # ----------------------------- Create the routes -------------------------

    i = 0
    for train in route:
        x_routes = []
        y_routes = []

        # for station in train.get_stations():
        #     station_x, station_y = station.get_position()
        #     # if (station_x, station_y) not in b:
        #     #     station_x -= 0.001
        #     #     station_y -= 0.001
        #     x_routes.append(station_x)
        #     y_routes.append(station_y)

        last_station = train.get_stations()[0]
        for connection in train.get_connections():
            times_passed = connection.get_times_passed()
            last_x, last_y = last_station.get_position()
            if times_passed > 1:
                # move the connection
                pass
            x_routes.append(last_x)
            y_routes.append(last_y)
            last_station = connection.get_destination(last_station)
        last_x, last_y = last_station.get_position()
        x_routes.append(last_x)
        y_routes.append(last_y)

        data += [go.Scattermapbox(
            lon=x_routes,
            lat=y_routes,
            mode = 'markers+lines',
            marker=dict(color=train.get_color(), opacity=0.5),
            # width=i,
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
                showlegend=False
            )
        )

    # include a map
    fig.update_layout(
        margin = {'l':0,'t':0, 'b':0, 'r':0},
        mapbox = {
            'center': {'lon': 5.2, 'lat': 52.2},
            'style': 'carto-positron',
            'zoom': 7
        }
    )


    if save_as_png:
        fig.write_image(f'code/output/create_gif/fig{num}.jpeg')
    else:
        fig.show()


    # app = dash.Dash()
    # app.layout = html.Div([
    #     dcc.Graph(figure=fig, style={'width': '90vh', 'height': '90vh'})
    # ])

    # app.run_server(debug=True, use_reloader=False)

def create_gif(name: str):
    frames = []
    files = glob.glob(f"code/output/create_gif/*.jpeg")
    # print(files)
    for image in files:
        # print(image)
        i = Image.open(image)
        # print(i)
        frames.append(i)
    # print(frames)
    frame_one = frames[0]
    frame_one.save(f"{name}.gif", append_images=frames[1:],
                optimize=False, save_all=True, duration=100, loop=0)