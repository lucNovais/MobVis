import pandas as pd

from mobvis.utils import Timer
from mobvis.metrics.utils.IMetric import IMetric

class VisitOrder(IMetric):
    def __init__(self, trace_loc):
        """ Class that corresponds to the Visit Order (VISO) spatiotemporal metric.

        ### Attributes:

        `trace_loc` (pandas.DataFrame): Geo-locations DataFrame of the trace. Extracted by the mobvis.metrics.utils.Locations module.
        """

        self.name = 'VISO'

        self.trace_loc = trace_loc.loc[trace_loc.gl == True]
        self.initial_id = int(self.trace_loc.id[0])

    @Timer.timed
    def extract(self, proc_num=None, return_dict=None):
        """ Method that extracts the Visit Order metric.

        ### Returns:

        `viso_df` (pandas.DataFrame): DataFrame containing the Visit Order data as shown below:
            - id: Node identifier
            - x: x position where the node entered the Geo-location
            - y: y position where the node entered the Geo-location
            - sl: Geo-location identifier
            - visit_order: Integer that corresponds to the order of the visited Geo-location
            - timestamp: Timestamp where the node entered the Geo-location
            
        """
        print('\nExtracting the Visit Order...')

        index = 1
        current_sl = 0
        current_id = self.initial_id
        viso_df = self.trace_loc.rename({'index': 'visit_order'}, axis=1).copy()

        for i, row in self.trace_loc.iterrows():
            if row.id == current_id:
                if row.sl == current_sl and row.gl:
                    pass
                elif row.gl:
                    current_sl = row.sl
                    index += 1
            else:
                current_id = row.id
                current_sl = 0
                index = 1

            viso_df.loc[i, 'visit_order'] = index
        
        viso_df = viso_df.drop(['gl'], axis=1)
        viso_df = viso_df.drop_duplicates(subset=['id', 'sl'])

        print('Visit Order extracted successfully!')

        if proc_num != None:
            return_dict[proc_num] = viso_df
        else:
            return viso_df
