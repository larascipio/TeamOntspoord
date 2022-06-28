"""
mean_plot.py

Programmeertheorie - minor programmeren
Lara, Tim, Eva

- Make a boxplot of the mean of the quality.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def plot_analysis(temps, mean: list, std: list, colors: tuple, name: str, xaxis: str, yaxis: str, title: str):
    """Plot the mean with the standard deviation."""
    
    # create the data for the plots
    x = temps
    x_rev = x[::-1]
    y_mean = mean
    y_high = [y_mean[i] + std[i] for i in range(len(y_mean))]
    y_low = [y_mean[i] - std[i] for i in range(len(y_mean))]
    y_low = y_low[::-1]

    fig = go.Figure()

    # # add the standard deviation to the figure
    # fig.add_trace(go.Scatter(
    #     x=x+x_rev,
    #     y=y_high+y_low,
    #     fill='toself',
    #     fillcolor=f'rgba({colors[0]}, {colors[1]}, {colors[2]}, 0.2)',
    #     line_color='rgba(255,255,255,0)',
    #     showlegend=False,
    #     name=name,
    # ))

    # # add the mean to the figure
    # fig.add_trace(go.Scatter(
    #     x=x, y=y_mean,
    #     line_color=f'rgb({colors[0]}, {colors[1]}, {colors[2]})',
    #     name=name
    # ))



    fig.add_trace(go.Scatter(
        x=temps,
        y=mean,
        mode='markers',
        error_y=dict(
            type='data',
            array=std,
            visible=True
        )
    ))

    fig.update_xaxes(type='log')

    fig.update_layout(
        title=title,
        xaxis_title=xaxis,
        yaxis_title=yaxis
        )

    fig.show()

def simple_plot(y1,name1,y2,name2,y3,name3):
    x = [i for i in range(len(y1))]
    # fig = go.Figure()
    fig = make_subplots(specs=[[{'secondary_y':True}]])
    fig.add_trace(go.Scatter(
        x=x, y=y1, name=name1), secondary_y=False
    )
    fig.add_trace(go.Scatter(
        x=x, y=y2, name=name2), secondary_y=True
    )
    fig.add_trace(go.Scatter(
        x=x, y=y3, name=name3), secondary_y=False
    )
    fig.show()

def plot_3d(df, xname:str, yname:str, zname:str):
    fig = px.scatter_3d(df, x=xname, y=yname, z=zname,
        color=zname)
    fig.update_layout(scene=dict(xaxis=dict(type='log')))
    fig.show()