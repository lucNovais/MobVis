import pandas as pd

from mobvis.utils import Timer
from mobvis.metrics.utils.IMetric import IMetric

class TravelTime(IMetric):
    def __init__(self, trace_loc):
        """ Class that corresponds to the Travel Time (TRVT) temporal metric.

        ### Attributes:

        `trace_loc` (pandas.DataFrame): Geo-locations DataFrame of the trace. Extracted by the mobvis.metrics.utils.Locations module.
        """

        self.name = 'TRVT'

        self.trace_loc = trace_loc.loc[trace_loc.gl == True]

    @Timer.timed
    def extract(self, proc_num=None, return_dict=None):
        """ Method that extracts the Travel Time metric.

        ### Returns:

        `trvt_df` (pandas.DataFrame): DataFrame containing the Travel Time data as shown below:
            - id: Node identifier
            - init_sl: Initial Geo-location where the node was
            - final_sl: Final Geo-location of the travel
            - t_exit: Timestamp when the node left the initial Geo-location
            - t_arrival: Timestamp when the node arrived the final Geo-location
            - travel_time: Time spent on the travel
        """
        print('\nExtracting the Travel Time...')

        trvt_df = pd.DataFrame(columns=['id', 'init_sl', 'final_sl', 't_exit', 't_arrival', 'travel_time'])

        for index, row in enumerate(self.trace_loc.iterrows()):
            if index == 0:
                pass
            else:
                if row[1].id != prev_row.id:
                    pass
                elif row[1].sl != prev_row.sl:
                    trvt = row[1].timestamp - prev_row.timestamp

                    new_row = pd.DataFrame({
                        'id': [row[1].id],
                        'init_sl': [prev_row.sl],
                        'final_sl': [row[1].sl],
                        't_exit': [prev_row.timestamp],
                        't_arrival': [row[1].timestamp],
                        'travel_time': [trvt]
                    })
                    
                    trvt_df = pd.concat([trvt_df, new_row], ignore_index=True)

            prev_row = row[1]
                    
        print('Travel Distance extracted successfully!\n')

        if proc_num != None:
            return_dict[proc_num] = trvt_df
        else:
            return trvt_df
