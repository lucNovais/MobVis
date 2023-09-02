import pandas as pd

from mobvis.utils import Timer
from mobvis.metrics.utils.IMetric import IMetric

class ContactDuration(IMetric):
    def __init__(self, filename, trace, df_type, req_dataframes):
        """ Class that corresponds to the Contact Duration (CODU) social metric.
        """

        self.contacts_df = req_dataframes['contacts_df']

        super().__init__(filename, trace, df_type)

    @Timer.timed
    def extract(self):
        print('\nExtracting the Contact Time...')



        print('\nContact Time extracted successfully!')
