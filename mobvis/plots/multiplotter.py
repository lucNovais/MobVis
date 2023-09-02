from multiprocessing.pool import ThreadPool

from mobvis.plots.metric_plotter import *
from mobvis.plots.spatial_plotter import *

def histogram_multiplotter(metric_dfs, metric_names, differ_nodes=False, specific_users=None,
                           users_to_display=None, hnorm=None, show_title=True, show_y_label = True,
                           img_width=600, img_height=560, title=' - Histogram'):
    """ Generates histograms for the given metric DataFrames using threads.

    ### Parameters:

    `metric_dfs` (pandas.DataFrame): DataFrames corresponding to the extracted metrics from some mobvis.metrics module.
    `metric_names` (str): Names of the metrics on the DataFrames. (Ex.: TRVD, RADG, VIST etc).
    `differ_nodes` (bool): If each node needs to be differed on the plot.
    `specific_users` (int[]): Specific nodes ids that the plot will use data from.
    `users_to_display` (int): Maximum number of ids to be considered on the plot.
    `hnorm` (str): Plotly histogram norm. See https://plotly.github.io/plotly.py-docs/generated/plotly.express.histogram.html
    `show_title` (bool): If the graph title should appear on the image.
    `show_y_label` (bool): If the y label should appear on the image.
    `img_width` (float): Width of the generated image.
    `img_height` (float): Height of the generated image.
    `title` (str): Title of the graph.

    ### Returns:

    `fig` (plotly.graph_objects.Figure): Plotly interactive histogram generated with the given data and parameters.
    """
    args = [(metric_dfs[i], metric_names[i], differ_nodes[i], specific_users[i]) for i in range(len(metric_dfs))]

    plots = []

    with ThreadPool() as pool:
        for result in pool.starmap(plot_metric_histogram, args):
            plots.append(result)
    
    return plots
