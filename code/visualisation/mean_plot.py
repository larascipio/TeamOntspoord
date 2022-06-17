import plotly.graph_objects as go

def plot_analysis(temps, mean: list, std: list, colors: tuple, name: str):
    """Plot the mean with the standard deviation."""
    
    # create the data for the plots
    x = temps
    x_rev = x[::-1]
    y_mean = mean
    y_high = [y_mean[i] + std[i] for i in range(len(y_mean))]
    y_low = [y_mean[i] - std[i] for i in range(len(y_mean))]
    y_low = y_low[::-1]

    fig = go.Figure()

    # add the standard deviation to the figure
    fig.add_trace(go.Scatter(
        x=x+x_rev,
        y=y_high+y_low,
        fill='toself',
        fillcolor=f'rgba({colors[0]}, {colors[1]}, {colors[2]}, 0.2)',
        line_color='rgba(255,255,255,0)',
        showlegend=False,
        name=name
    ))

    # add the mean to the figure
    fig.add_trace(go.Scatter(
        x=x, y=y_mean,
        line_color=f'rgb({colors[0]}, {colors[1]}, {colors[2]})',
        name=name
    ))

    fig.update_xaxes(type='log')

    fig.show()