from distutils.log import warn
import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

from mobvis.utils.Utils import fix_size_conditions
from mobvis.utils.Utils import find_ranges

def plot_trace(trace, specific_users=None, differ_nodes=True, users_to_display=None,
               show_title=True, show_y_label=True, title='Trace Movements', md='markers',
               img_width=600, img_height=560, **kwargs):
    """ Function to generate a figure of a trace movements with a heatmap indicating the timestamps.

    ### Parameters:

    `trace` (pandas.DataFrame): DataFrame corresponding to the trace.
    `specific_users` (int[]): If specified, the plot will consider only the movements of the nodes on the list.
    `differ_nodes` (bool): If true, each node on the trace will have a different symbol.
    `users_to_display` (int): Number of users that will appear on the plot.
    `show_title` (bool): If the title will appear on the image.
    `show_y_label` (bool): If the y label should appear on the image.
    `title` (str): Title of the graph.
    `md` (str): Plot mode. Supported modes are markers, markers+lines and lines.
    `img_width` (int): Image width.
    `img_height` (int): Image height.
    `**kwargs` (dictionary): Dictionary that can contain specific Plotly arguments.

    ### Returns:

    `fig` (plotly.scatter): Plotly figure corresponding to the trace movements.
    """

    plt_trace = fix_size_conditions(
        df=trace,
        limit=15,
        users_to_display=users_to_display,
        specific_users=specific_users
    )

    if differ_nodes:
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
        hover_data=['id', 'timestamp'],
        **kwargs
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


def plot_trace3d(trace, specific_users=None, differ_nodes=True, users_to_display=None,
                 show_title=True, show_y_label=True, title='Trace Movements', md='markers+lines',
                 img_width=600, img_height=560, **kwargs):
    """ Function to generate a figure of a trace movements in three dimensions, with a heatmap.

    ### Parameters:

    `trace` (pandas.DataFrame): DataFrame corresponding to the trace.
    `specific_users` (int[]): If specified, the plot will consider only the movements of the nodes on the list.
    `differ_nodes` (bool): If true, each node on the trace will have a different symbol.
    `users_to_display` (int): Number of users that will appear on the plot.
    `show_title` (bool): If the title will appear on the image.
    `show_y_label` (bool): If the y label should appear on the image.
    `title` (str): Title of the graph.
    `md` (str): Plot mode. Supported modes are markers, markers+lines and lines.
    `img_width` (int): Image width.
    `img_height` (int): Image height.
    `**kwargs` (dictionary): Dictionary that can contain specific Plotly arguments.

    ### Returns:

    `fig` (plotly.scatter3d): Plotly figure corresponding to the trace movements in three dimensions.
    """

    plt_trace = fix_size_conditions(
        df=trace,
        limit=15,
        users_to_display=users_to_display,
        specific_users=specific_users
    )

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
        hover_data=['id', 'timestamp'],
        **kwargs
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

def plot_density(trace, specific_users=None, users_to_display=None, xrange=None, yrange=None,
                 show_title=True, show_y_label=True, title='Density',
                 img_width=600, img_height=560, **kwargs):
    """ Function that generates a figure corresponding to the density of the trace movements.

    ### Parameters:

    `trace` (pandas.DataFrame): DataFrame corresponding to the trace.
    `specific_users` (int[]): If specified, the plot will consider only the locations visited by the nodes on the list.
    `users_to_display` (int): Number of users that will appear on the plot.
    `xrange` (float): Specify the range of the x axis.
    `yrange` (float): Specify the range of the y axis.
    `show_title` (bool): If the title will appear on the image.
    `show_y_label` (bool): If the y label should appear on the image.
    `title` (str): Title of the graph.
    `img_width` (int): Image width.
    `img_height` (int): Image height.
    `**kwargs` (dictionary): Dictionary that can contain specific Plotly arguments.

    ### Returns:

    `fig` (plotly.graph_objects.Figure): Plotly figure with the density of the trace markers on the map.
    """
    plt_trace = fix_size_conditions(
        df=trace,
        limit=15,
        users_to_display=users_to_display,
        specific_users=specific_users
    )

    fig = go.Figure()

    if show_title:
        title_dict = {
            'text': title,
            'font_color': 'black',
            'font_size': 22,
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
            ),
            **kwargs
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

def plot_visit_order(trace_viso, specific_users=None, users_to_display=None, show_title=True,
                     show_y_label=True, title='Visit Order', img_width=600, img_height=560, **kwargs):
    """ Function that generates a figure with the visited Geo-locations in order.

    ### Parameters:

    `trace_viso` (pandas.DataFrame): Visit order DataFrame extracted by the mobvis.metrics.spatial.VisitOrder class.
    `specific_users` (int[]): If specified, the plot will consider only the locations visited by the nodes on the list.
    `users_to_display` (int): Number of users that will appear on the plot.
    `show_title` (bool): If the title will appear on the image.
    `show_y_label` (bool): If the y label should appear on the image.
    `title` (str): Title of the graph.
    `img_width` (int): Image width.
    `img_height` (int): Image height.
    `**kwargs` (dictionary): Dictionary that can contain specific Plotly arguments.

    ### Returns:

    `fig` (plotly.scatter): Plotly figure corresponding to the Geo-locations with labels of the Visit Order metric.
    """

    print('\nGenerating the Visit Order plot...')

    plt_trace = fix_size_conditions(
        df=trace_viso,
        limit=15,
        users_to_display=users_to_display,
        specific_users=specific_users
    )

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
        },
        **kwargs
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
        textfont_size=14
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

def plot_locations(sl_centers, specific_users=[0], differ_nodes=False,
                   users_to_display=None, limit_locations=False, show_title=True, show_y_label=True,
                   title='Geo-locations', img_width=600, img_height=560, **kwargs):
    """ Function to generate a figure of the stay locations visited by a node or a group of nodes.

    ### Parameters:

    `sl_centers` (pandas.DataFrame): DataFrame corresponding to the center of the Geo-locations.
    `specific_users` (int[]): If specified, the plot will consider only the locations visited by the nodes on the list.
    `differ_nodes` (bool): If true, each node on the trace will have a different symbol.
    `users_to_display` (int): Number of users that will appear on the plot.
    `limit_locations` (bool): If true, limit the Geo-locations that will appear on the plot for the 10 locations with most
                              time spent by the users (remember to use this with the travel time metric and specify the nodes that will appear by
                              the `users_to_display` parameter).
    `title` (str): Title of the graph.
    `img_width` (int): Image width.
    `img_height` (int): Image height.

    ### Returns:

    `fig` (plotly.scatter): Plotly figure corresponding to the stay locations visited by the node/nodes.
    """

    sl_centers = fix_size_conditions(
        df=sl_centers,
        limit=10,
        users_to_display=users_to_display,
        specific_users=specific_users
    )

    [xrange, yrange] = find_ranges(sl_centers)

    if differ_nodes:
        smap = 'id'
        img_width += 140
    else:
        smap = None

    if limit_locations:
        trace_vist = kwargs.get('visit_time')
        aux_vist = pd.DataFrame()

        try:
            for i in specific_users:
                aux_vist = trace_vist.loc[trace_vist.id==i]
        except AttributeError:
            warn("WARNING: The `limit_locations` attribute can not be passed as `True` with no `visit_time` dataframe included on the kwargs!")
            return

        most_time_spent = aux_vist.sort_values(['visit_time'], ascending=False).head(10)['sl'].values
        most_relevant_loc = pd.DataFrame(columns=['sl', 'x', 'y'])

        for location in most_time_spent:
            append_row = sl_centers.loc[sl_centers.sl==location]
            most_relevant_loc = pd.concat([most_relevant_loc, append_row], ignore_index=True)
            
        sl_centers = most_relevant_loc
        sl_centers.sl = sl_centers.sl.astype('int').astype('str')

    fig = px.scatter(
        sl_centers,
        x='x',
        y='y',
        color='sl',
        symbol=smap,
        labels= {
            'timestamp': 'Timestamp',
            'sl': 'Geo<br>Location'
        },
        hover_data=['sl']
    )
    
    customdata = np.stack((sl_centers['sl']))

    fig.update_traces(
        marker_size=10,
        hovertemplate =
            '<i><b>Geo Location</b></i><br><br>' +
            'Location ID: %{customdata[0]}<br>' +
            'x: %{x}<br>' +
            'y: %{y}'
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
        legend_font_size=20,
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

# def plot_animated_movements(trace, initial_id, specific_users=None, differ_nodes=True, users_to_display=None, speed_multiplier=1,
#                             show_title=True, show_y_label=True, title='Trace Animated Movements', md='markers', img_width=600, img_height=560, **kwargs):
#     original_size = trace.id.size

#     plt_trace = fix_size_conditions(original_size, initial_id, trace, 10, users_to_display, specific_users)

#     if differ_nodes:
#         cmap = 'id'
#         img_width += 140
#     else:
#         cmap = None

#     min_x = plt_trace.x.min()
#     min_y = plt_trace.y.min()

#     max_x = plt_trace.x.max()
#     max_y = plt_trace.y.max()

#     plt_trace.id = plt_trace.id.astype(str)

#     [xrange, yrange] = find_ranges(plt_trace)

#     fig = px.scatter(
#         trace,
#         x='x',
#         y='y',
#         color=cmap,
#         color_discrete_sequence=px.colors.qualitative.Vivid,
#         animation_frame='timestamp',
#         animation_group='id',
#         labels={
#             'id': 'User ID'
#         },
#         range_x=[min_x, max_x],
#         range_y=[min_y, max_y],
#         title=title
#     )

#     fig.update_traces(
#         marker=dict(size=6)
#     )

    # if with_hl:
    #     hldf = utils.fix_size_conditions(original_size, hl_df, 5, users_to_display, user_ids)

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

    # if show_title:
    #     title_dict = {
    #         'text': title,
    #         'font_color': 'black',
    #         'x': 0.5,
    #         'y': 0.98
    #     }
    #     margin_dict = dict(t=40, b=25)
    # else:
    #     title_dict = None
    #     margin_dict = dict(t=10, b=25)

    # if not show_y_label:
    #     fig.update_yaxes(visible=False)
    #     margin_dict['l'] = 10
    #     margin_dict['r'] = 10
    # else:
    #     margin_dict['l'] = 12
    #     margin_dict['r'] = 10

    # fig.update_layout(
    #     width=img_width,
    #     height=img_height,
    #     title=title_dict,
    #     font=dict(
    #         size=16
    #     ),
    #     title_font_size=22,
    #     coloraxis_colorbar=dict(
    #         yanchor='top',
    #         xanchor='left',
    #         y=1.009,
    #         x=1
    #     ),
    #     margin=margin_dict
    # )

    # fig.update_coloraxes(
    #     colorbar_thickness=15,
    #     colorbar_tickfont_size=20,
    #     colorbar_title_font_size=22
    # )

    # if differ_nodes:
    #     fig.update_layout(
    #         margin=dict(l=220),
    #         legend=dict(
    #             yanchor='top',
    #             xanchor='left',
    #             x=-0.52,
    #             borderwidth=1,
    #             bgcolor="#E2E2E2"
    #     ))

    # fig.update_yaxes(
    #     tickfont=dict(size=22),
    #     title_font_size=26,
    #     range=yrange
    # )
    # fig.update_xaxes(
    #     tickfont=dict(size=22),
    #     title_font_size=26,
    #     range=xrange
    # )

    # fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1 * speed_multiplier
    # fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 2 * speed_multiplier

    # return fig
