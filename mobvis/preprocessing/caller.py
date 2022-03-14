from mimetypes import init
from stat import S_IWOTH
from turtle import title
import pandas as pd

from mobvis.preprocessing import extractor as mc_extractor
from mobvis.plots import metric_plotter, spatial_plotter

def call_plots(plot, metric_type, metric_dataframe, parsed_df, initial_id, locations=None):
    """Calls plot methods depending on which plots were requested in input.
    
    Parameters:

    plots (str[]): List of keywords that correspond to plot types.
    filename (str): Name of the original file (trace).
    metrics (str[]): List of keywords that correspond to different metrics.
    """

    if 'STATISTICAL' == plot:
        return generate_statistical(metric_type, metric_dataframe, initial_id)
    if 'SPATIAL' == plot:
        return generate_spatial(parsed_df, locations, initial_id)

def generate_statistical(metric_type, metric_dataframe, initial_id):
    print('\nGenerating all statistical plots...')

    if len(metric_dataframe) > 0:
        histogram = metric_plotter.plot_metric_histogram(
            metric_dataframe,
            initial_id=initial_id,
            metric_type=metric_type,
            differ_nodes=False,
            show_title=False,
            show_y_label=False,
            max_users=max(metric_dataframe[metric_dataframe.columns[0]])
        )

        boxplot = metric_plotter.boxplot_metric(
            metric_dataframe,
            initial_id=initial_id,
            metric_type=metric_type,
            show_title=False,
            show_y_label=True,
            max_users=max(metric_dataframe[metric_dataframe.columns[0]])
        )

        dist = metric_plotter.plot_metric_dist(
            metric_dataframe,
            initial_id=initial_id,
            metric_type=metric_type,
            max_users=max(metric_dataframe[metric_dataframe.columns[0]]),
            show_title=False,
            show_y_label=False,
            differ_nodes=False
        )

        return [histogram, boxplot, dist]
    else:
        return None

def generate_spatial(parsed_df, locations, initial_id):
    print('\nGenerating all spatial plots...')

    trace_styloc = locations[0]
    styloc_centers = locations[1]

    trace = spatial_plotter.plot_trace(
        parsed_df,
        initial_id=initial_id,
        differ_nodes=False,
        nodes_list=[20],
        show_title=False,
        show_y_label=True,
        md="markers"
    )

    # anim_trace = spatial_plotter.plot_animated_movements(
    #     parsed_df,
    #     df_type='bm',
    #     nodes_list=[0],
    #     differ_nodes=False,
    #     title="San Francisco Cab - Animated Trace"
    # )

    trace3d = spatial_plotter.plot_trace3d(
        parsed_df,
        initial_id=initial_id,
        differ_nodes=False,
        nodes_list=[20],
        show_title=False,
        show_y_label=True,
        md="markers+lines"
    )

    sty_loc = spatial_plotter.plot_locations(
        trace_styloc,
        styloc_centers,
        initial_id=initial_id,
        show_title=False,
        show_y_label=True,
        nodes_list=[20]
    )

    nodes_density = spatial_plotter.plot_density(
        trace_styloc,
        initial_id=initial_id,
        max_users=10,
        show_title=False,
        show_y_label=False
    )

    return [trace, trace3d, sty_loc, nodes_density]

def special_plots(special_metric, data, initial_id):
    if special_metric == 'VISO':
        visit_order = spatial_plotter.plot_visit_order(
            data,
            initial_id=initial_id,
            show_title=False,
            nodes_list=[20]
        )
        return visit_order