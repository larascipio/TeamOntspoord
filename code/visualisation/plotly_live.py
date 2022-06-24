import plotly.graph_objects as go
import plotly.express as px
import os


class Live_Plot():
    def __init__(self, rails):
        # print('see the plot at:')
        # path = os.getcwd()
        # print(f'{path}\code\output\live_plot.html')
        self._rails = rails

        # ----------------------------- Create the connections --------------------
        self._railsdata = []
        distances = []
        for connection in rails.get_connections():
            x = []
            y = []
            for station in connection._stations:
                x.append(station._x)
                y.append(station._y)
            self._railsdata.append(go.Scattermapbox(
                lon=x,
                lat=y,
                mode = 'lines',
                marker=dict(color='black', size=1),
                hoverinfo='skip'
            ))

            distances.append(connection._distance)

        # ----------------------------- Create the stations -----------------------
        x_stations = []
        y_stations = []
        name = []
        for station in rails.get_stations().values():
            x_stations.append(station._x)
            y_stations.append(station._y)
            name.append(station._name)
        # print(x, y)
        # data.append(go.Scatter(x=x_stations, y=y_stations, mode='markers', hovertext=name, hoverinfo='text'))
        self._railsdata.append(go.Scattermapbox(
            lon=x_stations, 
            lat=y_stations, 
            mode='markers', 
            hovertext=name, 
            hoverinfo='text'))
        
        # ----------------------------- create the colors -------------------------
        self._color = px.colors.qualitative.Plotly + px.colors.qualitative.Plotly

        self._layout = go.Layout(
                title_text='A map of all trainstations and connections', 
                hovermode='closest',
                showlegend=False
            )
        
        self.update_fig(None)


    def update_fig(self, num):

        # ----------------------------- Create the lines --------------------------
        data = self._railsdata

        
        i = 0
        for train in self._rails.get_trains():
            x_routes = []
            y_routes = []
            for station in train.get_stations():
                station_x, station_y = station.get_position()
                x_routes.append(station_x)
                y_routes.append(station_y)

            data += [go.Scattermapbox(
                lon=x_routes,
                lat=y_routes,
                mode = 'lines',
                marker=dict(color=self._color[i%len(self._color)]),
                hoverinfo='skip'
            )]
            i += 1

        # create the figure
        fig = go.Figure(
            data=data,
            layout=self._layout
        )

        # include a map
        fig.update_layout(
            margin = {'l':0,'t':0, 'b':0, 'r':0},
            mapbox = {
                'center': {'lon': 5.2, 'lat': 52.1},
                'style': 'open-street-map',
                'zoom': 6.4
            }
        )

        # fig.write_html('code/output/live_plot.html')
        fig.write_image(f'code/output/create_gif/fig{num}.jpeg')