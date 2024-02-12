import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plotly_dual_axis(df,  x="timestamp", y1="", y2="", title="", x_title="Time", y1_title="", y2_title="", different_y_axes_scale=True):

    if y1_title == "":
        y1_title = y1
    if y2_title == "":
        y2_title = y2

    y1_label=y1
    y2_label=y2

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(
            x=df[x], 
            y=df[y1], 
            hovertemplate = '[label]<br>Timestamp: %{x|%Y-%m-%d %H:%M:%S}<br>Value: %{y}<extra></extra>'.replace('[label]', y1_label),
            name=y1_label),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=df[x],
            y=df[y2],
            hovertemplate = '[label]<br>Timestamp: %{x|%Y-%m-%d %H:%M:%S}<br>Value: %{y}<extra></extra>'.replace('[label]', y2_label),
            name=y2_label),
        secondary_y=different_y_axes_scale,
    )

    # Add figure title
    fig.update_layout(
        title_text=title
    )

    # Set x-axis title
    fig.update_xaxes(title_text=x_title)

    # Set y-axes titles
    fig.update_yaxes(title_text=y1_title, secondary_y=False)
    if different_y_axes_scale==True:
        fig.update_yaxes(title_text=y2_title, secondary_y=True)

    # fig.show()



    return fig


def plotly_dual_axis_multi_y2(df,  x="timestamp", y1="", list_y2=[], title="", x_title="Time", y1_title="", y2_title="", different_y_axes_scale=True, scaler=None):

    if y1_title == "":
        y1_title = y1


    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    
    y1_label=y1
    # fig.add_trace(
    #     go.Scatter(mode='lines+markers', x=df[x], y=df[y1], name=y1_label),
    #     secondary_y=False,
    # )
    fig.add_trace(
        go.Scatter(
            mode='lines+markers',
            x=df[x].values, 
            y=df[y1].values, 
            hovertemplate = "[label]<br>Timestamp: %{x|%Y-%m-%d %H:%M:%S}<br>Value: %{y}<extra></extra>".replace('[label]', y1_label),
            name=y1_label),
        secondary_y=False,
    )

    for y2 in list_y2:
        y2_label=y2
        
        if scaler == None:
            y_series = df[y2].values
        else:
            if scaler == 'minmax':
                y_series = MinMaxScaler().fit_transform(pd.DataFrame(df[y2])).reshape(-1, )
            elif scaler == 'standard':
                y_series = StandardScaler().fit_transform(pd.DataFrame(df[y2])).reshape(-1, )
            else:
                y_series = df[y2].values
                print('#### Wrong normalization setting!')

        fig.add_trace(
            go.Scatter(
                mode='lines',
                x=df[x], 
                y=y_series, 
                hovertemplate = "[label]<br>Timestamp: %{x|%Y-%m-%d %H:%M:%S}<br>Value: %{y}<extra></extra>".replace('[label]', y2_label),
                name=y2_label),
            secondary_y=different_y_axes_scale,
        )


    # Add figure title
    fig.update_layout(
        title_text=title
    )

    # Set x-axis title
    fig.update_xaxes(title_text=x_title)

    # Set y-axes titles
    
    fig.update_yaxes(title_text=y1_title, secondary_y=False)
    if different_y_axes_scale == True:
        fig.update_yaxes(title_text=y2_title, secondary_y=True)

    # fig.show()

    return fig




def plotly_multi_timeseries(df,  x="timestamp", list_y=[], title="", x_title="Time", y_title="", scaler=None):


    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": False}]])

    # Add traces

    # fig.add_trace(
    #     go.Scatter(mode='lines+markers', x=df[x], y=df[y1], name=y1_label),
    #     secondary_y=False,
    # )
    # fig.add_trace(
    #     go.Scatter(
    #         mode='lines+markers',
    #         x=df[x], 
    #         y=df[y1], 
    #         hovertemplate = "[label]<br>Timestamp: %{x|%Y-%m-%d %H:%M:%S}<br>Value: %{y}<extra></extra>".replace('[label]', y1_label),
    #         name=y1_label),
    #     secondary_y=False,
    # )



    for y in list_y:
        y_label=y
        # fig.add_trace(
        #     go.Scatter(mode='lines', x=df[x], y=df[y2], name=y2_label),
        #     secondary_y=True,
        # )
        if scaler == None:
            y_series = df[y].values
        else:
            if scaler == 'minmax':
                y_series = MinMaxScaler().fit_transform(pd.DataFrame(df[y])).reshape(-1, )
            elif scaler == 'standard':
                y_series = StandardScaler().fit_transform(pd.DataFrame(df[y])).reshape(-1, )
            else:
                y_series = df[y].values
                print('#### Wrong normalization setting!')

        fig.add_trace(
            go.Scatter(
                mode='lines',
                x=df[x].values, 
                y=y_series, 
                hovertemplate = "[label]<br>Timestamp: %{x|%Y-%m-%d %H:%M:%S}<br>Value: %{y}<extra></extra>".replace('[label]', y_label),
                name=y_label)
        )


    # Add figure title
    fig.update_layout(
        title_text=title
    )

    # Set x-axis title
    fig.update_xaxes(title_text=x_title)

    # Set y-axes titles
    
    fig.update_yaxes(title_text=y_title, secondary_y=False)

    # fig.show()


    return fig
