import pandas as pd

from mobvis.utils import Timer
from mobvis.metrics.utils.IMetric import IMetric

class VisitTime(IMetric):
    def __init__(self, trace_loc):
        """Class that corresponds to the Travel Time temporal metric.

        Attributes:

        `trace_loc` (pandas.DataFrame): Geo-locations DataFrame of the trace. Extracted by the mobvis.metrics.utils.Locations module.
        """

        self.trace_loc = trace_loc

    @Timer.timed
    def extract(self):
        """Method that extracts the Visit Time metric.

        Returns:

        `vist_df` (pandas.DataFrame): DataFrame containing the Visit Time data as shown below:
            id: Node identifier
            timestamp: Timestamp where the node arrived at the Geo-location
            sl: Geo-location visited by the node
            visit_time: Time spent on that specific Geo-location
        """

        print('Extracting the Visit Time...')

        vist_df = pd.DataFrame(columns=['id', 'timestamp', 'sl', 'visit_time'])

        for index, row in enumerate(self.trace_loc.iterrows()):
            curr_row = row[1]
            if index == 0:
                prev_row = curr_row
                arrival_time = prev_row.timestamp
            else:
                if curr_row.id == prev_row.id:
                    if curr_row.sl == prev_row.sl:
                        pass
                    else:
                        depearture_time = prev_row.timestamp
                        visit_time = depearture_time - arrival_time

                        vist_df = vist_df.append({
                            'id': prev_row.id,
                            'timestamp': prev_row.timestamp,
                            'sl': prev_row.sl,
                            'visit_time': visit_time
                        }, ignore_index=True)

                        arrival_time = curr_row.timestamp
                else:
                    prev_row = row[1]
                    arrival_time = prev_row.timestamp

            prev_row = curr_row

        print('Visit Time extracted successfully!\n')

        return vist_df

    def export(self):
        pass