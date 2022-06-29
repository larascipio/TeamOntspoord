import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio


def create_animation(railnet, save_as_png=False, num=0):

    # get the stations and connections
    stations = list(railnet.get_stations().values())
    connectionlist = list(railnet.get_connections())

    # create the colours for the trains
    route = railnet.get_trains()

    # ----------------------------- Create the connections ---------------------

    data = []

    for connection in connectionlist:
        x = []
        y = []
        for station in connection.get_stations():
            x.append(station._x)
            y.append(station._y)
        # data.append(go.Scatter(x=x,y=y, marker=dict(color='blue', size=1), hoverinfo='skip'))
        data.append(go.Scattermapbox(
            lon=x,
            lat=y,
            mode='markers+lines',
            marker=dict(color='lightgray', size=1),
            hoverinfo='skip'
        ))

        if connection.get_times_passed() > 1:
            data.append(go.Scattermapbox(
                lon=[(x[0]+x[1])/2],
                lat=[(y[0]+y[1])/2],
                mode='text',
                hovertext=connection.get_times_passed(),
                hoverinfo='text',
                textfont=dict(size=16, color='black')
            ))

    # ----------------------------- Create the stations ------------------------

    # create a marker for each station
    x_stations = []
    y_stations = []
    name = []
    for station in stations:
        x_stations.append(station._x)
        y_stations.append(station._y)
        name.append(station._name)

    # add the data to the map
    data.append(go.Scattermapbox(
        lon=x_stations,
        lat=y_stations,
        mode='markers',
        marker=dict(color='pink'),
        hovertext=name,
        hoverinfo='text',
    ))

    # ----------------------------- Create the routes -------------------------

    for train in route:

        # create a line from station to station
        x_routes = []
        y_routes = []

        for station in train.get_stations():
            station_x, station_y = station.get_position()
            x_routes.append(station_x)
            y_routes.append(station_y)

        # last_station = train.get_stations()[0]
        # last_x, last_y = last_station.get_position()
        # for connection in train.get_connections():
        #     # create every connection
        #     new_station = connection.get_destination(last_station)
        #     new_x, new_y = new_station.get_position()

        #     # times_passed = connection.get_times_passed()
        #     # if times_passed > 1:
        #     #     # remove the connection
        #     #     connection.remove()
        #     #     helling = (last_y-new_y)/(last_x-new_x)
        #     #     print(helling)
        #     #     change = 0.005
        #     #     last_y += -1*change
        #     #     new_y += -1*change
        #     #     last_x += change*helling
        #     #     new_x += change*helling

        #     x_routes.append(last_x)
        #     y_routes.append(last_y)
        #     last_station = new_station
        #     last_x, last_y = (new_x, new_y)
        # last_x, last_y = last_station.get_position()
        # x_routes.append(last_x)
        # y_routes.append(last_y)

        # add the route to the map
        data += [go.Scattermapbox(
            lon=x_routes,
            lat=y_routes,
            mode='lines',
            line=dict(color=train.get_color(), width=2),
            hoverinfo='skip'

        )]

    # ----------------------------- Create the figure -------------------------

    # make the figure
    fig = go.Figure(
        data=data,
        layout=go.Layout(
            title_text='A map of all trainstations and connections',
            hovermode='closest',
            showlegend=False
        )
    )

    # include a map to the background
    fig.update_layout(
        margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
        mapbox={
            'center': {'lon': 5.2, 'lat': 52.2},
            'style': 'carto-positron',
            'zoom': 7
            # 'acces_token':
        }
    )

    fig.show()

    # if save_as_png:
    #     fig.write_image('code/output/fig.svg')
    #     pio.write_image(fig, f'code/output/fig1.svg')
    


def create_boxplot(df, title):
    """
    Create a boxplot of the different algorithms.
    """

    fig = px.box(df, y=df.columns, title=title)
    fig.update_xaxes(title='Algorithm')
    fig.update_yaxes(title='Quality')

    # write the image to a 
    pio.write_image(fig, 'output/new_fig.png', width=1*300, height=1*300)
    fig.show()
