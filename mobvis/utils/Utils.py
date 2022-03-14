import pandas as pd
import numpy as np
from scipy import stats

from math import radians, cos, sin, asin, sqrt


def fix_size_conditions(original_size, initial_id, df, limit, max_points, user_ids):
    """Function for filtering the trace to the specified or default conditions.

    Parameters:

    `original_size` (int): Number of nodes of the original trace.
    `initial_id` (int): First node identifier value of the trace.
    `df` (pandas.DataFrame): Oiriginal trace.
    `limit` (int): Limit of nodes to be displayed on the image.
    `max_points` (int): Number of users that will appear on the plot.
    `user_ids` (int[]): List of specific users to be plotted.

    Returns:

    `df` (pandas.DataFrame): Filtered DataFrame. 
    """

    if not max_points and not user_ids and original_size > limit:
        df = filter_df(df, min_index=initial_id, max_index=initial_id + limit)
    elif original_size < limit:
        df = filter_df(df, min_index=initial_id, max_index=initial_id + original_size)
    elif max_points:
        df = filter_df(df, min_index=initial_id, max_index=initial_id + max_points)
    else:
        df = filter_df(df, uids_list=user_ids)

    return df

def filter_df(full_df, min_index=None, max_index=None, uids_list=None):
    df = pd.DataFrame()

    if not uids_list:
        for i in range(int(min_index), int(max_index)):
            df = df.append(full_df.loc[full_df.id == i], ignore_index=True)
    else:
        for i in uids_list:
            df = df.append(full_df.loc[full_df.id == i], ignore_index=True)

    return df

def find_ranges(trace):
    """Function for finding the range of the plot axes based on the x and y values.

    Parameters:

    `trace` (pandas.DataFrame): Trace that will be plotted.

    Returns:

    `xrange` (float[]): List containing the minimum and maximum x axis values of the plot.
    `yrange` (float[]): List containing the minimum and maximum y axis values of the plot.
    """

    plus_x = (max(trace.x.values) - min(trace.x.values)) / 10
    plus_y = (max(trace.y.values) - min(trace.y.values)) / 10

    sum = (plus_x + plus_y) / 2

    xrange = [min(trace.x.values) - sum, max(trace.x.values) + sum]
    yrange = [min(trace.y.values) - sum, max(trace.y.values) + sum]

    return [xrange, yrange]

# http://www.jtrive.com/determining-histogram-bin-width-using-the-freedman-diaconis-rule.html
def freedman_diaconis(data, returnas="width"):
    """
    Use Freedman Diaconis rule to compute optimal histogram bin width. 
    ``returnas`` can be one of "width" or "bins", indicating whether
    the bin width or number of bins should be returned respectively. 


    Parameters
    ----------
    data: np.ndarray
        One-dimensional array.

    returnas: {"width", "bins"}
        If "width", return the estimated width for each histogram bin. 
        If "bins", return the number of bins suggested by rule.
    """
    data = np.asarray(data, dtype=np.float_)
    IQR  = stats.iqr(data, rng=(25, 75), scale=1.0, nan_policy="omit")
    N    = data.size
    bw   = (2 * IQR) / np.power(N, 1/3)

    if returnas=="width":
        result = bw
    else:
        datmin, datmax = data.min(), data.max()
        datrng = datmax - datmin
        result = int((datrng / bw) + 1)

    return(result)

# https://janakiev.com/blog/gps-points-distance-python/
def haversine(lat1, lon1, lat2, lon2):
    """Function for calculating the Haversine distance of two points.

    Parameters:

    `lat1` (float): Latitude of the first point.
    `lon1` (float): Longitude of the first point.
    `lat2` (float): Latitude of the second point.
    `lon2` (float): Longitude of the second point.

    Returns:

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