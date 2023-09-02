import pandas as pd

from mobvis.utils import Timer
from mobvis.metrics.utils.IMetric import IMetric

from concurrent.futures import ThreadPoolExecutor

from scipy.spatial import distance
from mobvis.utils.Utils import haversine

# TODO: Distancia de cada posição do trace. d(pk, pk+1) p/ todo p
# TODO: Velocidade media

class TravelDistance(IMetric):
    def __init__(self, trace_loc, dist_type):
        """ Class that corresponds to the Travel Distance (TRVD) spatial metric.

        ### Attributes:

        `trace_loc` (pandas.DataFrame): Geo-locations DataFrame of the trace extracted by the mobvis.metrics.utils.Locations module.
        `dist_type` (str): Distance formula. Supported types are: Haversine and Euclidean.
        """
        
        self.name = 'TRVD'

        # self.trace_loc = trace_loc.loc[trace_loc.gl == True] if len(trace_loc) == 1 else [trace_loc[i].loc[trace_loc[i].gl == True] for i in range(0, len(trace_loc))]
        self.trace_loc = trace_loc.loc[trace_loc.gl == True]
        self.dist_type = dist_type

    @Timer.timed
    def extract(self, proc_num=None, return_dict=None):
        """ Method that extracts the Travel Distance metric.

        ### Returns:

        `trvd_df` (pandas.DataFrame): DataFrame containing the Travel Distance data as shown below:
            - id: Node identifier
            - travel_distance: Distance of the travel
            - init_sl: Initial geo-location
            - final_sl: Final geo-location
            - ix: Initial x position
            - iy: Initial y postiion
            - fx: Final x position
            - fy: Final y position
        """
        print('\nExtracting the Travel Distance...')

        trvd_df = pd.DataFrame(columns=[
            'id',
            'travel_distance',
            'init_sl',
            'final_sl',
            'ix',
            'iy',
            'fx',
            'fy'
        ])
        
        if self.dist_type.lower() == 'haversine':
            trvd_df = self.haversine_iterator(trvd_df)
        elif self.dist_type.lower() == 'euclidean':
            trvd_df = self.euclidean_iterator(trvd_df)
                    
        print('Travel Distance extracted successfully!\n')

        if proc_num != None:
            return_dict[proc_num] = trvd_df
        else:
            return trvd_df

    def haversine_iterator(self, trvd_df):
        """Method that finds the Travel Distance based on the Haversine formula.
        """
        for index, row in enumerate(self.trace_loc.iterrows()):
            if index == 0:
                pass
            else:
                if row[1].id != prev_row.id:
                    pass
                elif row[1].sl != prev_row.sl:
                    xA = prev_row.x
                    xB = row[1].x
                    yA = prev_row.y
                    yB = row[1].y
                    trvd = haversine(xA, yA, xB, yB)
                    
                    new_row = pd.DataFrame({
                        'id': [row[1].id],
                        'travel_distance': [trvd],
                        'init_sl': [prev_row.sl],
                        'final_sl': [row[1].sl],
                        'ix': [prev_row.x],
                        'iy': [prev_row.y],
                        'fx': [row[1].x],
                        'fy': [row[1].y]
                    })
                    trvd_df = pd.concat([trvd_df, new_row], ignore_index=True)

            prev_row = row[1]
        
        return trvd_df

    def euclidean_iterator(self, trvd_df):
        """ Method that finds the Travel Distance based on the Euclidean formula.
        """
        for index, row in enumerate(self.trace_loc.iterrows()):
            if index == 0:
                pass
            else:
                if row[1].id != prev_row.id:
                    pass
                elif row[1].sl != prev_row.sl:
                    xA = prev_row.x
                    xB = row[1].x
                    yA = prev_row.y
                    yB = row[1].y
                    trvd = distance.euclidean((xA, yA), (xB, yB))
                    
                    new_row = pd.DataFrame({
                        'id': [row[1].id],
                        'travel_distance': [trvd],
                        'init_sl': [prev_row.sl],
                        'final_sl': [row[1].sl],
                        'ix': [prev_row.x],
                        'iy': [prev_row.y],
                        'fx': [row[1].x],
                        'fy': [row[1].y]
                    })
                    trvd_df = pd.concat([trvd_df, new_row], ignore_index=True)

            prev_row = row[1]
        
        return trvd_df
