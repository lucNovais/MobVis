from distutils.log import warn
import pandas as pd
import numpy as np
from scipy import stats

from math import radians, cos, sin, asin, sqrt


def fix_size_conditions(df, limit, users_to_display, specific_users):
    """ Function for filtering the trace to the specified or default conditions.

    ### Parameters:

    `df` (pandas.DataFrame): Original trace/metric DataFrame.
    `limit` (int): Limit of nodes to be displayed on the image.
    `users_to_display` (int): Number of users that will appear on the plot.
    `specific_users` (int[]): List of specific users to be plotted.

    ### Returns:

    `df` (pandas.DataFrame): Fixed DataFrame. 
    """

    if 'id' in df.columns:
        original_size = df.id.size
        try:
            initial_id = get_trace_initial_id(df)
        except IndexError as err:
            raise err

        if not limit:
            limit = original_size
    else:
        return df

    if not users_to_display and not specific_users and original_size >= limit:
        if original_size > limit:
            warn(f'WARNING: The number of nodes exceeds the default limit of the plot. Only the first {limit} nodes will appear on screen. If you want to increase this number or change this to display all the nodes, please set the `users_to_display` parameter, or specify the nodes to display with the `specific_users` parameter.')
        df = filter_df(df, min_index=initial_id, max_index=initial_id + limit)
    elif original_size < limit:
        df = filter_df(df, min_index=initial_id, max_index=initial_id + original_size)
    elif users_to_display:
        df = filter_df(df, min_index=initial_id, max_index=initial_id + users_to_display)
    else:
        df = filter_df(df, ids_list=specific_users)

    return df

def filter_df(full_df, min_index=None, max_index=None, ids_list=None):
    """ Removes all the nodes that should not appear on the fixed DataFrame.
    """
    fixed_df = pd.DataFrame()

    if not ids_list:
        for i in range(int(min_index), int(max_index)):
            fixed_df = pd.concat([fixed_df, full_df.loc[full_df.id == i]], ignore_index=True)
    else:
        for i in ids_list:
            fixed_df = pd.concat([fixed_df, full_df.loc[full_df.id == i]], ignore_index=True)

    return fixed_df

def find_ranges(trace):
    """ Function for finding the range of the plot axes based on the x and y values.

    ### Parameters:

    `trace` (pandas.DataFrame): Trace that will be plotted.

    ### Returns:

    `xrange` (float[]): List containing the minimum and maximum x axis values of the plot.
    `yrange` (float[]): List containing the minimum and maximum y axis values of the plot.
    """

    plus_x = (max(trace.x.values) - min(trace.x.values)) / 10
    plus_y = (max(trace.y.values) - min(trace.y.values)) / 10

    sum = (plus_x + plus_y) / 2

    xrange = [min(trace.x.values) - sum, max(trace.x.values) + sum]
    yrange = [min(trace.y.values) - sum, max(trace.y.values) + sum]

    return [xrange, yrange]

def config_metric_plot(metric_name, differ_nodes):
    """ Function that takes the metric type and defines the name of the column that needs to be used
        for generating the statistical plots.

    ### Parameters:

    `metric_name` (str): Name of the metric.
    `differ_nodes` (bool): True if the nodes needs to be differentiated on the plot, False otherwise.

    ### Returns:

    `x_values` (str): Name of the column that will generate the histograms/boxplots etc.
    `cmap` (str): If set, the plot needs to differentiate which parts of the graph correspond to which nodes.
    `title_complement` (str): Metric name to be used on the figure title. 

    """
    if metric_name == 'TRVD':
        x_values = 'travel_distance'
        title_complement = 'Travel Distance'
    elif metric_name == 'RADG':
        x_values = 'radius_of_gyration'
        title_complement = 'Radius of Gyration'
    elif metric_name == 'VIST':
        x_values = 'visit_time'
        title_complement = 'Visit Time'
    elif metric_name == 'TRVT':
        x_values = 'travel_time'
        title_complement = 'Travel Time'
    elif metric_name == 'INCO':
        x_values = 'intercontact_time'
        title_complement = 'Intercontact Time'

    if differ_nodes:
        cmap = 'id'
    else:
        cmap = None

    return [x_values, cmap, title_complement]

def get_trace_initial_id(metric_df):
    """ Gets the value of the first identifier of the trace.

    ### Parameters:

    `metric_df` (pandas.DataFrame): DataFrame corresponding to the metric extracted.

    ### Returns:

    `initial_id` (int): First integer that represents a identifier of the given trace.
    """

    if 'id' in metric_df.columns:
        try:
            initial_id = metric_df.id.values[0]
        except IndexError as err:
            warn("WARNING: Something went wrong while extracting the given metric! Plot cannot be generated.")
            raise err
    else:
        initial_id = metric_df.id1.values[0]

    return initial_id

# http://www.jtrive.com/determining-histogram-bin-width-using-the-freedman-diaconis-rule.html
def freedman_diaconis(data, returnas="width"):
    """
    Use Freedman Diaconis rule to compute optimal histogram bin width. 
    ``returnas`` can be one of "width" or "bins", indicating whether
    the bin width or number of bins should be returned respectively. 


    ### Parameters
    ----------
    data: np.ndarray
        One-dimensional array.

    ### returnas: {"width", "bins"}
        If "width", return the estimated width for each histogram bin. 
        If "bins", return the number of bins suggested by rule.
    """
    data = np.asarray(data, dtype=np.float_)
    IQR  = stats.iqr(data, rng=(25, 75), scale=1.0, nan_policy="omit")
    N    = data.size
    bw   = (2 * IQR) / np.power(N, 1/3)

    if returnas=="width":
        if bw > 0:
            result = bw
        else:
            result = None
    else:
        datmin, datmax = data.min(), data.max()
        datrng = datmax - datmin
        try:
            result = int((datrng / bw) + 1)
        except OverflowError:
            warn("WARNING: OverflowError while trying to calculate the number of bins, check locations parameters...")

            result = 2

    print(result)

    return(result)

# https://janakiev.com/blog/gps-points-distance-python/
def haversine(lat1, lon1, lat2, lon2):
    """Function for calculating the Haversine distance of two points.

    ### Parameters:

    `lat1` (float): Latitude of the first point.
    `lon1` (float): Longitude of the first point.
    `lat2` (float): Latitude of the second point.
    `lon2` (float): Longitude of the second point.

    ### Returns:

    `distance` (float): Haversine distance of the two points.
    """

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lat1, lon1, lat2, lon2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r * 1000 # meters
