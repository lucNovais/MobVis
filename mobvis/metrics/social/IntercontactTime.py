import pandas as pd

from mobvis.utils import Timer
from mobvis.metrics.utils.IMetric import IMetric

class IntercontactTime(IMetric):
    def __init__(self, contacts_df):
        """Class that corresponds to the Inter-contact Time social metric.

        Attributes:

        `contacts_df` (pandas.DataFrame): Contacts between the trace nodes. Extracted by the mobvis.metrics.utils.Contacts module.
        """

        self.contacts_df = contacts_df


    @Timer.timed
    def extract(self):
        """Method that extracts the Intercontact Time metric.

        Returns:

        `inco_df` (pandas.DataFrame): DataFrame containing the Intercontact Time data as shown below:
            id1: Identifier of the first node
            id2: Identifier of the second node
            timestamp: Intercontact time of the two nodes
        """
        print('\nExtracting the Inter-contact Time...')

        self.contacts_df.sort_values(['id1', 'id2', 'timestamp'], inplace=True)

        inco_df = pd.DataFrame(columns=['id1', 'id2', 'intercontact_time'])
        prev_row = []
    
        for index, row in enumerate(self.contacts_df.iterrows()):
            if index != 0:
                if row[1].id1 == prev_row[1].id1 and row[1].id2 == prev_row[1].id2:
                    inco = row[1].timestamp - prev_row[1].timestamp
                    inco_df = inco_df.append({
                        'id1': row[1].id1,
                        'id2': row[1].id2,
                        'intercontact_time': inco
                    }, ignore_index=True)

            prev_row = row
            
        print('\nInter-contact Time extracted successfully!')
        return inco_df

    def export(self):
        pass