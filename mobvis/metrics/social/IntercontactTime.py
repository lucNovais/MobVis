import pandas as pd

from mobvis.utils import Timer
from mobvis.metrics.utils.IMetric import IMetric

class IntercontactTime(IMetric):
    def __init__(self, contacts_df):
        """ Class that corresponds to the Inter-contact Time (INCO) social metric.

        ### Attributes:

        `contacts_df` (pandas.DataFrame): Contacts between the trace nodes. Extracted by the mobvis.metrics.utils.Contacts module.
        """

        self.name = 'INCO'

        self.contacts_df = contacts_df


    @Timer.timed
    def extract(self):
        """ Method that extracts the Intercontact Time metric.

        ### Returns:

        `inco_df` (pandas.DataFrame): DataFrame containing the Intercontact Time data as shown below:
            - id1: Identifier of the first node
            - id2: Identifier of the second node
            - intercontact_time: Intercontact time of the two nodes
        """
        print('\nExtracting the Inter-contact Time...')

        self.contacts_df.sort_values(['id1', 'id2', 'timestamp'], inplace=True)

        inco_df = pd.DataFrame(columns=['id1', 'id2', 'intercontact_time'])
        prev_row = []
    
        for index, row in enumerate(self.contacts_df.iterrows()):
            if index != 0:
                if row[1].id1 == prev_row[1].id1 and row[1].id2 == prev_row[1].id2:
                    inco = row[1].timestamp - prev_row[1].timestamp
                    
                    if inco > 30:
                        # Considers that two contacts are different if they occurred at least 30 seconds apart
                        new_row = pd.DataFrame({
                            'id1': [row[1].id1],
                            'id2': [row[1].id2],
                            'intercontact_time': [inco]
                        })

                        inco_df = pd.concat([inco_df, new_row], ignore_index=True)

            prev_row = row
            
        print('\nInter-contact Time extracted successfully!')
        return inco_df
