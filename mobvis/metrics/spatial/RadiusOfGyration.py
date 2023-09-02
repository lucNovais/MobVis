from mobvis.utils.Utils import haversine
import pandas as pd

from mobvis.utils import Timer
from mobvis.metrics.utils.IMetric import IMetric

from scipy.spatial import distance

from math import sqrt

class RadiusOfGyration(IMetric):
    def __init__(self, trace, trace_loc, sl_centers, homes, dist_type):
        """ Class that corresponds to the Radius of Gyration (RADG) spatial metric.

        ### Attributes:

        `trace` (pandas.DataFrame): DataFrame corresponding to the parsed trace.
        `trace_loc` (pandas.DataFrame): Geo-locations DataFrame of the trace. Extracted by the mobvis.metrics.utils.Locations module.
        `sl_centers` (pandas.DataFrame): DataFrame containing the coordinates of the centers of each Geo-location. Extracted by the mobvis.metrics.utils.Locations module.
        `homes` (pandas.DataFrame): DataFrame containing the Home-locations of each node. Extracted by the mobvis.metrics.utils.HomeLocations module.
        `dist_type` (str): Distance formula. Supported types are: Haversine and Euclidean.
        """

        self.name = 'RADG'

        self.trace = trace
        self.trace_loc = trace_loc.loc[trace_loc.gl == True]
        self.sl_centers = sl_centers
        self.homes = homes
        self.dist_type = dist_type

    @Timer.timed
    def extract(self, proc_num=None, return_dict=None):
        """ Method that extracts the Radius of Gyration metric.

        ### Returns:

        `radg_df` (pandas.DataFrame): DataFrame containing the Radius of Gyration data as shown below:
            - id: Node identifier
            - home_location: Home location of the node
            - radius_of_gyration: Radius of Gyration of that specific node
        """
        print('\nExtracting the Radius of Gyration...')
        
        radg_df = pd.DataFrame(columns=['id', 'home_location', 'radius_of_gyration'])
    
        id_list = self.trace.id.unique()
    
        radg = 0
    
        for i in id_list:
            # Gets the current node home location
            home_location = (self.homes.loc[self.homes.id == i].x.values[0], self.homes.loc[self.homes.id == i].y.values[0])
            # Gets all the points visited by this specific node
            points = [(row[1].x, row[1].y) for row in self.trace.loc[self.trace.id == i].iterrows()]
        
            if self.dist_type.lower() == 'euclidean':
                radg = self.euclidean_radius_of_gyration_formula(points, home_location)
            elif self.dist_type.lower() == 'haversine':
                radg = self.haversine_radius_of_gyration_formula(points, home_location)
            new_row = pd.DataFrame({
                'id': [i],
                'home_location': [self.homes.loc[self.homes.id == i].home_location.values[0]],
                'radius_of_gyration': [radg]
            })

            radg_df = pd.concat([radg_df, new_row], ignore_index=True)

        print('Radius of Gyration extracted successfully!')

        if proc_num != None:
            return_dict[proc_num] = radg_df
        else:
            return radg_df

    def euclidean_radius_of_gyration_formula(self, points, home_location):
        """ Iterates over all the points passed and evaluates the Radius of Gyration formula
            using the given Home Location as the center of mass. The distance is calculated
            with the Euclidean formula.
        """
        total_sum = 0
        for point in points:
            total_sum += pow(distance.euclidean((point[0], point[1]), home_location), 2)

        radg = (1/len(points)) * total_sum
        radg = sqrt(radg)
        
        return radg

    def haversine_radius_of_gyration_formula(self, points, home_location):
        """ Iterates over all the points passed and evaluates the Radius of Gyration formula
            using the given Home Location as the center of mass. The distance is calculated
            with the Haversine formula.
        """
        total_sum = 0
        for point in points:
            total_sum += pow(haversine(point[0], point[1], home_location[0], home_location[1]), 2)
        radg = (1/len(points)) * total_sum
        radg = sqrt(radg)
        
        return radg
