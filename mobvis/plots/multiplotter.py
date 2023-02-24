from multiprocessing.pool import ThreadPool

from mobvis.plots.metric_plotter import *
from mobvis.plots.spatial_plotter import *

def histogram_multiplotter(metric_dfs, metric_names, differ_nodes=False, specific_users=None,
                           users_to_display=None, hnorm=None, show_title=True, show_y_label = True,
                           img_width=600, img_height=560, title=' - Histogram'):
    args = [(metric_dfs[i], metric_names[i], differ_nodes[i], specific_users[i]) for i in range(len(metric_dfs))]

    plots = []

    with ThreadPool() as pool:
        for result in pool.starmap(plot_metric_histogram, args):
            plots.append(result)
    
    return plots
