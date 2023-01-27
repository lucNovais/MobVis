import pandas as pd
import numpy as np

from scipy.spatial import distance
from mobvis.utils import Timer

from multiprocessing.pool import ThreadPool

from mobvis.utils.Utils import haversine

class Locations:
    def __init__(self):
        pass

    def stay_locations_euclidean(trace, max_D):
        """Finds the Stay-locations for each node based on the Euclidean distance formula.
        """
        sl_index = set()
        list_of_sl = []
        max_D = max_D
        pm = 0
        sl_index.add(pm)

        for i in range(1, trace.shape[0]):
            if distance.euclidean((trace.x[pm], trace.y[pm]), (trace.x[i], trace.y[i])) < max_D:
                sl_index.add(i)
            else:
                list_of_sl.append(sl_index)
                sl_index = set()
                sl_index.add(i)
                pm = i

        list_of_sl.append(sl_index)

        trace['sl'] = 0
        count_sl = 0
        for sl in list_of_sl:
            trace.loc[list(sl), 'sl'] = count_sl
            count_sl += 1
        return trace

    def stay_locations_haversine(cls, trace, max_D):
        """Finds the Stay-locations for each node based on the Haversine distance formula.
        """
        sl_index = set()
        list_of_sl = []
        max_D = max_D
        pm = 0
        sl_index.add(pm)

        for i in range(1, trace.shape[0]):
            if haversine(trace.x[pm], trace.y[pm], trace.x[i], trace.y[i]) < max_D:
                sl_index.add(i)
            else:
                list_of_sl.append(sl_index)
                sl_index = set()
                sl_index.add(i)
                pm = i

        list_of_sl.append(sl_index)

        trace['sl'] = 0
        count_sl = 0
        for sl in list_of_sl:
            trace.loc[list(sl), 'sl'] = count_sl
            count_sl += 1
        return trace

    def geo_locations(trace, pause_threshold):
        """Determinates if the Stay-locations found are also Geo-locations.
        """
        gl = trace.groupby('sl')['timestamp'].agg(np.ptp)
        gl = gl>60 * pause_threshold
        gl = gl.reset_index()
        gl.columns = ['sl', 'gl']
        
        trace = trace.merge(gl, left_on='sl', right_on='sl')
        
        return trace

    @classmethod
    def multifinder_locations(cls, traces, max_distances, pause_thresholds, dist_types):
        print('Finding locations for multiple traces:\n')

        locations = []
        args = [(traces[i], max_distances[i], pause_thresholds[i], dist_types[i]) for i in range(0, len(traces))]

        with ThreadPool() as pool:
            for result in pool.starmap(cls.find_locations, args):
                locations.append(result)
        
        return locations

    @classmethod
    @Timer.timed
    def find_locations(cls, trace, max_d, pause_threshold, dist_type):
        """Finds the Stay-locations and Geo-locations of all nodes of a trace.
        
        Params:

        `trace` (pandas.DataFrame): DataFrame corresponding to the parsed trace.
        `max_d` (float): Maximum distance to a region be considered a Stay-location.
        `pause_threshold` (float): Ammout of waiting time to the Stay-location be considered a Geo-location (in minutes).
        `dist_type` (str): Distance formula. Supported types are: Haversine and Euclidean.
        
        Returns:

        `trace_loc` (pandas.DataFrame): The original input trace with the stay and geo locations defined as new columns.
        `sl_centers` (pandas.DataFrame): The centers of the Stay-locations based on the value of all the points on that location.
        """
        print('Finding the stay and geo locations...')
        print(f'\nParameters:\nMax Distance: {max_d}\nPause Threshold: {pause_threshold}\nDistance Formula: {dist_type}\n')

        trace_loc = pd.DataFrame(columns=['id', 'x', 'y', 'sl', 'gl'])
        sl_centers = pd.DataFrame(columns=['id', 'sl', 'x', 'y'])

        initial_id = int(trace.id[0])

        for i in range(initial_id, trace.id.max() + 1):
            aux_trace = trace.loc[trace.id == i].reset_index()

            if dist_type.lower() == 'haversine':
                aux_trace = cls.stay_locations_haversine(cls, aux_trace, max_d)
            elif dist_type.lower() == 'euclidean':
                aux_trace = cls.stay_locations_euclidean(aux_trace, max_d)

            aux_trace = cls.geo_locations(aux_trace, pause_threshold)
            trace_loc =  pd.concat([trace_loc, aux_trace], ignore_index=True)
        
            aux_trace = trace_loc.loc[(trace_loc.gl == True) & (trace_loc.id == i)]

            x = aux_trace.groupby('sl').x.mean()
            y = aux_trace.groupby('sl').y.mean()
            max_x = aux_trace.groupby('sl').x.max()
            min_x = aux_trace.groupby('sl').x.min()
            max_y = aux_trace.groupby('sl').y.max()
            min_y = aux_trace.groupby('sl').y.min()

            sl_centers = pd.concat([sl_centers, pd.DataFrame({
                'id': i,
                'sl': x.index,
                'x': x.values,
                'y': y.values,
                'max_x': max_x.values,
                'min_x': min_x.values,
                'max_y': max_y.values,
                'min_y': min_y.values
            })], ignore_index=True)
            
        print(trace_loc)
        print('Locations found!')
        return [trace_loc, sl_centers]