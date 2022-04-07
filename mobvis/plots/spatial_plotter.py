import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

from mobvis.utils.Utils import fix_size_conditions
from mobvis.utils.Utils import find_ranges

def plot_trace(trace, initial_id, nodes_list=None, differ_nodes=True, number_of_nodes=None,
               show_title=True, show_y_label=True, title='Trace Movements', md='markers', img_width=600, img_height=560, **kwargs):
    """Function to generate a figure of a trace movements with a heatmap indicating the timestamps.

    Parameters:

    `trace` (pandas.DataFrame): DataFrame corresponding to the trace.
    `df_type` (str): String indicating the origin of the trace.
    `nodes_list` (int[]): If specified, the plot will consider only the movements of the nodes on the list.
    `differ_nodes` (bool): If true, each node on the trace will have a different symbol.
    `number_of_nodes` (int): Number of users that will appear on the plot.
    `title` (str): Title of the graph.
    `md` (str): Plot mode, default value will only plot the scatter markers.
    `img_width` (int): Image width.
    `img_height` (int): Image height.

    Returns:

    `fig` (plotly.scatter): Plotly figure corresponding to the trace movements.
    """
    original_size = trace.id.size

    # original_size, initial_id, df, limit, max_points, user_ids
    plt_trace = fix_size_conditions(original_size, initial_id, trace, 10, number_of_nodes, nodes_list)

    if differ_nodes:
        # If the user chooses to differ the nodes by their ids, every user will have a different symbol.
        smap = 'id'
        img_width += 140
    else:
        smap = None

    [xrange, yrange] = find_ranges(plt_trace)

    fig = px.scatter(
        plt_trace,
        x='x',
        y='y',
        color='timestamp',
        opacity=0.6,
        symbol=smap,
        labels= {
            'timestamp': 'Timestamp',
            'id': 'Node ID'
        },
        title=title,
        hover_data=['id', 'timestamp']
    )

    if show_title:
        title_dict = {
            'text': title,
            'font_color': 'black',
            'x': 0.5,
            'y': 0.98
        }
        margin_dict = dict(t=40, b=25)
    else:
        title_dict = None
        margin_dict = dict(t=10, b=25)

    if not show_y_label:
        margin_dict['l'] = 12
        margin_dict['r'] = 10
        y_title = None
    else:
        margin_dict['l'] = 14
        margin_dict['r'] = 10
        y_title = 'y'

    fig.update_layout(
        width=img_width,
        height=img_height,
        title=title_dict,
        font=dict(
            size=16
        ),
        title_font_size=22,
        coloraxis_colorbar=dict(
            yanchor='top',
            xanchor='left',
            y=1.009,
            x=1
        ),
        yaxis_title=y_title,
        margin=margin_dict
    )

    fig.update_coloraxes(
        colorbar_thickness=15,
        colorbar_tickfont_size=20,
        colorbar_title_font_size=22
    )

    fig.update_yaxes(
        tickfont=dict(size=22),
        title_font_size=26,
        range=yrange
    )
    fig.update_xaxes(
        tickfont=dict(size=22),
        title_font_size=26,
        range=xrange
    )

    if differ_nodes:
        fig.update_layout(
            margin=dict(l=220),
            legend=dict(
                yanchor='top',
                xanchor='left',
                x=-0.52,
                borderwidth=1,
                bgcolor="#F8F8F8"
        ))

    customdata = np.stack((plt_trace['id'], plt_trace['timestamp']))

    fig.update_traces(
        marker_size=6,
        mode=md,
        hovertemplate =
            '<i><b>Movement Marker</b></i><br><br>' +
            'Node ID: %{customdata[0]}<br>' +
            'x: %{x}<br>' +
            'y: %{y}<br><br>' +
            'Timestamp: %{customdata[1]}<br>'
    )

    print('\nSuccessfully generated plot!')

    return fig


def plot_trace3d(trace, initial_id, nodes_list=None, differ_nodes=True, number_of_nodes=None,
                 show_title=True, show_y_label=True, title='Trace Movements', md='markers+lines', img_width=600, img_height=560, **kwargs):
    """Function to generate a figure of a trace movements in three dimensions, with a heatmap.

    Parameters:

    `trace` (pandas.DataFrame): DataFrame corresponding to the trace.
    `df_type` (str): String indicating the origin of the trace.
    `nodes_list` (int[]): If specified, the plot will consider only the movements of the nodes on the list.
    `differ_nodes` (bool): If true, each node on the trace will have a different symbol.
    `number_of_nodes` (int): Number of users that will appear on the plot.
    `title` (str): Title of the graph.
    `md` (str): Plot mode, default value will only plot the scatter markers.
    `img_width` (int): Image width.
    `img_height` (int): Image height.

    Returns:

    `fig` (plotly.scatter3d): Plotly figure corresponding to the trace movements in three dimensions.
    """
    original_size = trace.id.size

    plt_trace = fix_size_conditions(original_size, initial_id, trace, 10, number_of_nodes, nodes_list)

    if differ_nodes:
        smap = 'id'
        img_width += 140
    else:
        smap = None

    [xrange, yrange] = find_ranges(plt_trace)

    fig = px.scatter_3d(
        plt_trace,
        x='x',
        y='y',
        z='timestamp',
        color='timestamp',
        labels= {
            'timestamp': 'Timestamp',
            'id': 'Node ID'
        },
        opacity=0.6,
        symbol=smap,
        width=img_width,
        height=img_height,
        title=title,
        hover_data=['id', 'timestamp']
    )

    customdata = np.stack((plt_trace['id'], plt_trace['timestamp']))

    fig.update_traces(
        marker_size=4,
        mode=md,
        hovertemplate =
            '<i><b>Movement Marker</b></i><br><br>' +
            'Node ID: %{customdata[0]}<br>' +
            'x: %{x}<br>' +
            'y: %{y}<br><br>' +
            'Timestamp: %{z}<br>'
    )
    if show_title:
        title_dict = {
            'text': title,
            'font_color': 'black',
            'x': 0.5,
            'y': 0.98
        }
        margin_dict = dict(t=40, b=25)
    else:
        title_dict = None
        margin_dict = dict(t=10, b=25)

    if not show_y_label:
        fig.update_yaxes(visible=False)
        margin_dict['l'] = 10
        margin_dict['r'] = 10
    else:
        margin_dict['l'] = 12
        margin_dict['r'] = 10

    fig.update_layout(
        width=img_width,
        height=img_height,
        title=title_dict,
        font=dict(
            size=16
        ),
        title_font_size=22,
        coloraxis_colorbar=dict(
            yanchor='top',
            xanchor='left',
            y=1.009,
            x=1
        ),
        margin=margin_dict
    )

    fig.update_coloraxes(
        colorbar_thickness=15,
        colorbar_tickfont_size=20,
        colorbar_title_font_size=22
    )

    fig.update_yaxes(
        tickfont=dict(size=22),
        title_font_size=26,
        range=yrange
    )
    fig.update_xaxes(
        tickfont=dict(size=22),
        title_font_size=26,
        range=xrange
    )

    if differ_nodes:
        fig.update_layout(
            margin=dict(l=220),
            legend=dict(
                yanchor='top',
                xanchor='left',
                x=-0.52,
                borderwidth=1,
                bgcolor="#E2E2E2"
        ))

    print('\nSuccessfully generated plot!')

    return fig

def plot_locations(trace, sl_centers, initial_id, nodes_list=[0], number_of_nodes=None, limit_locations=False,
                  show_title=True, show_y_label=True, title='Stay Locations', img_width=600, img_height=560, **kwargs):
    """Function to generate a figure of the stay locations visited by a node or a group of nodes.

    Parameters:

    `trace` (pandas.DataFrame): DataFrame corresponding to the trace.
    `sl_centers` (pandas.DataFrame): DataFrame corresponding to the center of the stay locations.
    `df_type` (str): String indicating the origin of the trace.
    `nodes_list` (int[]): If specified, the plot will consider only the locations visited by the nodes on the list.
    `differ_nodes` (bool): If true, each node on the trace will have a different symbol.
    `number_of_nodes` (int): Number of users that will appear on the plot.
    `title` (str): Title of the graph.
    `img_width` (int): Image width.
    `img_height` (int): Image height.

    Returns:

    `fig` (plotly.scatter): Plotly figure corresponding to the stay locations visited by the node/nodes.
    """
    # TODO: Fix this plot.

    original_size = trace.id.size

    print(trace.head())

    plt_trace = fix_size_conditions(original_size, initial_id, trace, 10, number_of_nodes, nodes_list)

    print(plt_trace.head())

    sl_centers = fix_size_conditions(original_size, initial_id, sl_centers, 10, number_of_nodes, nodes_list)

    [xrange, yrange] = find_ranges(trace)

    if limit_locations:
        trace_vist = kwargs.get('visit_time')
        aux_vist = pd.DataFrame()

        for i in nodes_list:
            aux_vist = trace_vist.loc[trace_vist.id==i]

        most_time_spent = aux_vist.sort_values(['visit_time'], ascending=False).head(10)['sl'].values
        most_relevant_loc = pd.DataFrame(columns=['sl', 'x', 'y'])

        for location in most_time_spent:
            append_row = sl_centers.loc[sl_centers.sl==location]
            most_relevant_loc = most_relevant_loc.append({
                'sl': append_row.sl.values[0],
                'x': append_row.x.values[0],
                'y': append_row.y.values[0]
            }, ignore_index=True)
            
        sl_centers = most_relevant_loc
        sl_centers.sl = sl_centers.sl.astype('int').astype('str')

    fig = px.scatter(
        sl_centers,
        x='x',
        y='y',
        # symbol='sl',
        # color='timestamp',
        color='sl',
        labels= {
            'timestamp': 'Timestamp',
            'sl': 'Geo<br>Location'
        },
        hover_data=['sl']
    )
    
    customdata = np.stack((plt_trace['sl']))

    fig.update_traces(
        marker_size=10,
        hovertemplate =
            '<i><b>Geo Location</b></i><br><br>' +
            'Location ID: %{customdata[0]}<br>' +
            'x: %{x}<br>' +
            'y: %{y}'
    )

    # fig.add_trace(go.Scatter(
    #     x=sl_centers.x,
    #     y=sl_centers.y,
    #     mode='lines',
    #     name='Stay Location Center',
    #     line=dict(
    #         color='rgba(0, 0, 0, 0.15)',
    #         width=2
    #     ),
    #     showlegend=False
    # ))
    
    # for i in range(0, len(sl_centers)):
    #     fig.add_shape(
    #         type='circle',
    #         xref='x', yref='y',
    #         x0=sl_centers.iloc[i].min_x,
    #         y0=sl_centers.iloc[i].min_y,
    #         x1=sl_centers.iloc[i].max_x,
    #         y1=sl_centers.iloc[i].max_y,
    #         opacity=0.12,
    #         fillcolor='black'
    #     )

    if show_title:
        title_dict = {
            'text': title,
            'font_color': 'black',
            'x': 0.5,
            'y': 0.98
        }
        margin_dict = dict(t=40, b=25)
    else:
        title_dict = None
        margin_dict = dict(t=10, b=25)

    if not show_y_label:
        fig.update_yaxes(visible=False)
        margin_dict['l'] = 10
        margin_dict['r'] = 10
    else:
        margin_dict['l'] = 12
        margin_dict['r'] = 10

    fig.update_layout(
        width=img_width,
        height=img_height,
        title=title_dict,
        font=dict(
            size=16
        ),
        title_font_size=22,
        coloraxis_colorbar=dict(
            yanchor='top',
            xanchor='left',
            y=1.009,
            x=1
        ),
        legend_font_size=24,
        legend_title_font_size=22,
        margin=margin_dict
    )

    fig.update_yaxes(
        tickfont=dict(size=22),
        title_font_size=24,
        range=yrange
    )
    fig.update_xaxes(
        tickfont=dict(size=22),
        title_font_size=24,
        range=xrange
    )

    print('\nSuccessfully generated plot!')

    return fig

def plot_density(trace, initial_id, nodes_list=None, number_of_nodes=None, xrange=None, yrange=None,
                show_title=True, show_y_label=True, title='Density', md='markers', img_width=600, img_height=560, **kwargs):
    """Function that generates a figure corresponding to the density of the trace movements.

    Parameters:

    `trace` (pandas.DataFrame): DataFrame corresponding to the trace.
    `df_type` (str): String indicating the origin of the trace.
    `nodes_list` (int[]): If specified, the plot will consider only the locations visited by the nodes on the list.
    `number_of_nodes` (int): Number of users that will appear on the plot.
    `title` (str): Title of the graph.
    `img_width` (int): Image width.
    `img_height` (int): Image height.    

    Returns:

    `fig` (plotly.figure_factory.create_2d_density): Plotly figure corresponding to the density map of the trace.
    """

    original_size = trace.id.size

    plt_trace = fix_size_conditions(original_size, initial_id, trace, 10, number_of_nodes, nodes_list)

    fig = go.Figure()

    if show_title:
        title_dict = {
            'text': title,
            'font_color': 'black',
            'x': 0.5,
            'y': 0.98
        }
        margin_dict = dict(t=40, b=25)
    else:
        title_dict = None
        margin_dict = dict(t=10, b=25)

    fig.add_trace(go.Histogram2dContour(
            x=plt_trace.x,
            y=plt_trace.y,
            colorscale='Blues',
            reversescale=False,
            xaxis='x',
            yaxis='y',
            colorbar=dict(
                thickness=15,
                tickfont_size=20
            )
        ))
    fig.add_trace(go.Scatter(
            x=plt_trace.x,
            y=plt_trace.y,
            xaxis='x',
            yaxis='y',
            mode='markers',
            marker=dict(
                color='rgba(0,0,0,0.3)',
                size=4
            )
        ))

    fig.update_yaxes(
        title='y',
        tickfont=dict(size=22),
        title_font_size=26
    )
    fig.update_xaxes(
        title='x',
        tickfont=dict(size=22),
        title_font_size=26
    )

    if xrange and yrange:
        fig.update_yaxes(
            range=yrange
        )
        fig.update_xaxes(
            range=xrange
        )

    fig.add_trace(go.Histogram(
            y=plt_trace.y,
            xaxis='x2',
            marker=dict(
                color='rgba(0, 0, 0, 1)'
            )
        ))
    fig.add_trace(go.Histogram(
            x=plt_trace.x,
            yaxis='y2',
            marker=dict(
                color='rgba(0, 0, 0, 1)'
            )
        ))

    # if not show_y_label:
    #     fig.update_yaxes(visible=False)
    #     margin_dict['l'] = 10
    #     margin_dict['r'] = 10
    # else:
    #     margin_dict['l'] = 12
    #     margin_dict['r'] = 10

    fig.update_layout(
        autosize=False,
        title=title_dict,
        xaxis=dict(
            zeroline=False,
            domain=[0,0.85],
            showgrid=True
        ),
        yaxis = dict(
            zeroline=False,
            domain=[0,0.85],
            showgrid=True
        ),
        xaxis2=dict(
            zeroline=False,
            domain=[0.85,1],
            showgrid = False,
            showticklabels=False
        ),
        yaxis2=dict(
            zeroline=False,
            domain=[0.85,1],
            showgrid=False,
            showticklabels=False
        ),
        height=img_height,
        width=img_width,
        bargap=0,
        hovermode='closest',
        showlegend=False,
        margin=margin_dict
    )

    return fig

def plot_animated_movements(trace, initial_id, nodes_list=None, differ_nodes=True, number_of_nodes=None, speed_multiplier=1,
                            show_title=True, show_y_label=True, title='Trace Animated Movements', md='markers', img_width=600, img_height=560, **kwargs):
    original_size = trace.id.size

    plt_trace = fix_size_conditions(original_size, initial_id, trace, 10, number_of_nodes, nodes_list)

    if differ_nodes:
        cmap = 'id'
        img_width += 140
    else:
        cmap = None

    min_x = plt_trace.x.min()
    min_y = plt_trace.y.min()

    max_x = plt_trace.x.max()
    max_y = plt_trace.y.max()

    plt_trace.id = plt_trace.id.astype(str)

    [xrange, yrange] = find_ranges(plt_trace)

    fig = px.scatter(
        trace,
        x='x',
        y='y',
        color=cmap,
        color_discrete_sequence=px.colors.qualitative.Vivid,
        animation_frame='timestamp',
        animation_group='id',
        labels={
            'id': 'User ID'
        },
        range_x=[min_x, max_x],
        range_y=[min_y, max_y],
        title=title
    )

    fig.update_traces(
        marker=dict(size=6)
    )

    # if with_hl:
    #     hldf = utils.fix_size_conditions(original_size, hl_df, 5, number_of_nodes, user_ids)

    #     fig.add_trace(go.Scatter(
    #         x=hldf.lng,
    #         y=hldf.lat,
    #         mode='markers',
    #         opacity=0.25,
    #         marker=dict(
    #             color='Black',
    #             size=10,
    #         ),
    #         name='Home Location'
    #     ))

    if show_title:
        title_dict = {
            'text': title,
            'font_color': 'black',
            'x': 0.5,
            'y': 0.98
        }
        margin_dict = dict(t=40, b=25)
    else:
        title_dict = None
        margin_dict = dict(t=10, b=25)

    if not show_y_label:
        fig.update_yaxes(visible=False)
        margin_dict['l'] = 10
        margin_dict['r'] = 10
    else:
        margin_dict['l'] = 12
        margin_dict['r'] = 10

    fig.update_layout(
        width=img_width,
        height=img_height,
        title=title_dict,
        font=dict(
            size=16
        ),
        title_font_size=22,
        coloraxis_colorbar=dict(
            yanchor='top',
            xanchor='left',
            y=1.009,
            x=1
        ),
        margin=margin_dict
    )

    fig.update_coloraxes(
        colorbar_thickness=15,
        colorbar_tickfont_size=20,
        colorbar_title_font_size=22
    )

    if differ_nodes:
        fig.update_layout(
            margin=dict(l=220),
            legend=dict(
                yanchor='top',
                xanchor='left',
                x=-0.52,
                borderwidth=1,
                bgcolor="#E2E2E2"
        ))

    fig.update_yaxes(
        tickfont=dict(size=22),
        title_font_size=26,
        range=yrange
    )
    fig.update_xaxes(
        tickfont=dict(size=22),
        title_font_size=26,
        range=xrange
    )

    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1 * speed_multiplier
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 2 * speed_multiplier

    return fig

def plot_visit_order(trace_viso, initial_id, nodes_list=None, number_of_nodes=None,
                    show_title=True, show_y_label=True, title='Visit Order', md='markers', img_width=600, img_height=560, **kwargs):
    print('\nGenerating the Visit Order plot...')

    original_size = trace_viso.id.size

    plt_trace = fix_size_conditions(original_size, initial_id, trace_viso, 10, number_of_nodes, nodes_list)

    [xrange, yrange] = find_ranges(plt_trace)

    fig = px.scatter(
        plt_trace,
        x='x',
        y='y',
        color='timestamp',
        text='visit_order',
        labels={
            'timestamp': 'Timestamp',
            'visit_order': 'Visit<br>Order'
        }
    )

    fig.update_traces(
        textposition='top center'
    )

    if show_title:
        title_dict = {
            'text': title,
            'font_color': 'black',
            'x': 0.5,
            'y': 0.98
        }
        margin_dict = dict(t=40, b=25)
    else:
        title_dict = None
        margin_dict = dict(t=10, b=25)

    if not show_y_label:
        margin_dict['l'] = 10
        margin_dict['r'] = 10
        y_title = None
    else:
        margin_dict['l'] = 12
        margin_dict['r'] = 10
        y_title = 'y'

    fig.update_layout(
        width=img_width,
        height=img_height,
        title=title_dict,
        font=dict(
            size=16
        ),
        title_font_size=22,
        coloraxis_colorbar=dict(
            yanchor='top',
            xanchor='left',
            y=1.009,
            x=1
        ),
        yaxis_title=y_title,
        margin=margin_dict
    )

    fig.update_coloraxes(
        colorbar_thickness=15,
        colorbar_tickfont_size=20,
        colorbar_title_font_size=22
    )

    fig.update_traces(
        marker_size=6,
        textfont_size=12
    )
    
    fig.update_yaxes(
        tickfont=dict(size=22),
        title_font_size=26,
        range=yrange
    )
    fig.update_xaxes(
        tickfont=dict(size=22),
        title_font_size=26,
        range=xrange
    )

    return fig