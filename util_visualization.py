import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import functools
import datetime

end_datetime = datetime.datetime(2024, 4, 30, 23, 59, 59)

def time_limit(end_datetime):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if datetime.datetime.now() > end_datetime:
                raise Exception("The period of use has expired.")
            return func(*args, **kwargs)
        return wrapper
    return decorator


@time_limit(end_datetime)
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

@time_limit(end_datetime)
def plotly_dual_axis_multi_y2(df,  x="timestamp", y1="", list_y2=[], list_y2_add_text=[], title="", x_title="Time", y1_title="", y2_title="", different_y_axes_scale=True, scaler=None):

    if y1_title == "":
        y1_title = y1

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    y1_label=y1
    fig.add_trace(
        go.Scatter(
            mode='lines+markers',
            x=df[x].values, 
            y=df[y1].values, 
            hovertemplate = "[label]<br>Timestamp: %{x|%Y-%m-%d %H:%M:%S}<br>Value: %{y}<extra></extra>".replace('[label]', y1_label),
            name=y1_label),
        secondary_y=False,
    )

    for idx, y2 in enumerate(list_y2):
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
                name=f'{y2_label} {str(list_y2_add_text[idx])}'),
                # name=y2_label),
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



@time_limit(end_datetime)
def plotly_multi_timeseries(df,  x="timestamp", list_y=[], list_y_add_text=[], title="", x_title="Time", y_title="", scaler=None):


    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": False}]])

    # Add traces
    for idx, y in enumerate(list_y):
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
                name=f'{y_label} {str(list_y_add_text[idx])}'
                # name=y_label
                )
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



@time_limit(end_datetime)
def plotly_timeseries_per_entity(df, y, col_entity, x="timestamp", title="", x_title="Time", y_title="", scaler=None):


    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": False}]])

    # Add traces

    list_entity = df[col_entity].unique().tolist()

    for entity in list_entity:
        # fig.add_trace(
        #     go.Scatter(mode='lines', x=df[x], y=df[y2], name=y2_label),
        #     secondary_y=True,
        # )
        df_entity = df[df[col_entity] == entity]
        if scaler == None:
            y_series = df_entity[y].values
        else:
            if scaler == 'minmax':
                y_series = MinMaxScaler().fit_transform(pd.DataFrame(df_entity[y])).reshape(-1, )
            elif scaler == 'standard':
                y_series = StandardScaler().fit_transform(pd.DataFrame(df_entity[y])).reshape(-1, )
            else:
                y_series = df_entity[y].values
                print('#### Wrong normalization setting!')

        fig.add_trace(
            go.Scatter(
                mode='lines',
                x=df_entity[x].values, 
                y=y_series, 
                hovertemplate = "[label]<br>Timestamp: %{x|%Y-%m-%d %H:%M:%S}<br>Value: %{y}<extra></extra>".replace('[label]', entity),
                name=entity)
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


@time_limit(end_datetime)
def plot_kpi_with_correlated_metric(df_ts_kpi_and_metric, target_kpi, list_metric, start_time_end_time, timestamp_col='DateTime', title="", x_title="", y1_title="", y2_title="", top_N=3, scaler='standard', dual_axis=False):
## plot_kpi_with_correlated_metric(df_ts_kpi_and_metric, target_kpi, list_metric, start_time_end_time, timestamp_col='DateTime', title="", x_title="", y1_title="", y2_title="", top_N=2, scaler='standard', dual_axis=False)
    
    list_kpi_and_metric =  [target_kpi] + list_metric

    start_time = start_time_end_time[0]
    end_time = start_time_end_time[-1]

    df_ts_kpi_and_metric_filtered = df_ts_kpi_and_metric[
        (df_ts_kpi_and_metric[timestamp_col] >= start_time) & (df_ts_kpi_and_metric[timestamp_col] <= end_time) 
    ]

    df_corr = df_ts_kpi_and_metric_filtered[list_kpi_and_metric].corr()[target_kpi].drop([target_kpi], axis=0)

    list_top_N_correlated_metric = df_corr.abs().sort_values(ascending=False).iloc[0:top_N].index.to_list()

    list_str_corr = [f'(corr: {str(round(df_corr.loc[metric], 3))})' for metric in list_top_N_correlated_metric]
    
    fig = plotly_dual_axis_multi_y2(df_ts_kpi_and_metric_filtered,  x=timestamp_col, y1=target_kpi, list_y2=list_top_N_correlated_metric, list_y2_add_text=list_str_corr,
                                    title=title, x_title=x_title, y1_title=y1_title, y2_title=y2_title, different_y_axes_scale=dual_axis, scaler=scaler)


    return fig
