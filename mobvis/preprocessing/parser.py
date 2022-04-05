from tkinter.tix import COLUMN
import pandas as pd

from mobvis.utils import Timer
from mobvis.utils import Converters

SUPPORTED_TIMESTAMPS = [
    'datetime',
    'date',
    'time',
    'gps_time'
]

SUPPORTED_COORDINATES = [
    'lat',
    'lng',
    'long',
    'latitude',
    'longitude'
]

SUPPORTED_IDENTIFIERS = [
    'i',
    'id',
    'identifier',
    'uid',
    'node_id'
]

pd.set_option('display.precision', 10)

class Parser:
    def __init__(self):
        pass

    @classmethod
    @Timer.timed
    def parse(cls, raw_trace, is_ordered):
        """Method that converts the given DataFrame to the MobVis standard format.

        Parameters:

        `raw_trace` (pandas.DataFrame): Raw DataFrame containing the original trace.
        `is_ordered` (bool): 'True' if the rows of the raw DataFrame are ordered by the id and timestamps, `False` otherwise.

        Returns:

        `std_trace` (pandas.DataFrame): DataFrame corresponding to the parsed trace.
        """
        print('Parsing the given DataFrame...')

        # initial_id = int(raw_trace.id[0])

        std_trace = cls.check_columns(raw_trace)
        std_trace = cls.fix_timestamps(std_trace)

        if not is_ordered:
            std_trace = cls.order_rows(std_trace)

        print('Successfully parsed!\n')
        print(std_trace)

        return std_trace

    def check_columns(raw_trace):
        """Detects the columns informed for the raw trace and performs the procedures to convert
           them to the standard MobVis format.
        """
        default_order = ['id', 'timestamp', 'x', 'y']

        if len(raw_trace.columns) < 4:
            # Make this same thing but with exceptions handling
            print("\nERROR: Trace has less rows than expected")
            return
        elif len(raw_trace.columns) > 4:
            COLUMNS_FILTER = SUPPORTED_TIMESTAMPS + SUPPORTED_COORDINATES + SUPPORTED_IDENTIFIERS

            raw_trace = raw_trace[raw_trace.columns.intersection(COLUMNS_FILTER)]

        # Check if the timestamps column in the raw trace are on the datetime format, and consider some
        # possible names on the SUPPORTED_TIMESTAMPS array (case insensitive).
        raw_timestamp = [item for item in raw_trace.columns if item.lower() in SUPPORTED_TIMESTAMPS]
        if raw_timestamp:
            raw_timestamp = raw_timestamp[0]
            if type(raw_trace[raw_timestamp][0]) == str:
                raw_trace = Converters.convert_datetime(raw_trace, raw_timestamp)
            raw_trace.rename(columns={raw_timestamp: 'timestamp'}, inplace=True)

        # Check if the coordinates column in the raw trace are on the lat/long format, and consider some
        # possible names on the SUPPORTED_COORDINATES array (case insensitive).
        raw_coord = [item for item in raw_trace.columns if item.lower() in SUPPORTED_COORDINATES]
        if raw_coord:
            raw_trace.rename(columns={raw_coord[0]: 'y', raw_coord[1]: 'x'}, inplace=True)
            for i, col in enumerate(raw_trace.columns):
                if col == raw_coord[0]:
                    raw_trace.columns[i] = 'y'
                if col == raw_coord[1]:
                    raw_trace.columns[i] = 'x'

        # Sorts the dataframe columns according to the default library order
        std_trace_cols = [item for x in default_order for item in raw_trace.columns if item == x]
        # Sets the dataframe to the default order
        std_trace = raw_trace[std_trace_cols]
        
        return std_trace


    def order_rows(std_trace):
        """Order the rows based on the nodes identifiers and timestamps.
        """
        print('Sorting rows...')

        std_trace.sort_values(by=['id', 'timestamp'], inplace=True)

        return std_trace

    @classmethod
    def fix_timestamps(cls, std_trace):
        """Takes the smallest timestamp from the original trace and uses it as the zero timestamp.
           From there, it defines the other timestamps of the trace from the difference of the original
           timestamps and the smallest timestamp.
        """
        print('Fixing the timestamps...')
        std_trace['timestamp'] = std_trace['timestamp'].astype(float)
        std_trace['id'] = std_trace['id'].astype(int)
        std_trace['x'] = std_trace['x'].astype(float)
        std_trace['y'] = std_trace['y'].astype(float)

        fixed_timestamps = []

        # first_timestamp = std_trace.loc[std_trace.id == initial_id].timestamp.values[0]
        first_timestamp = std_trace['timestamp'].min()
        for i in std_trace.id.unique():
            current_timestamp = std_trace.loc[std_trace.id == i].timestamp.values[0]
            if current_timestamp < first_timestamp:
                first_timestamp = current_timestamp
        print(f'Shorter timestamp: {first_timestamp}')
        
        for row in std_trace.iterrows():
            fixed_timestamps.append(row[1].timestamp - first_timestamp)
            
        std_trace.drop('timestamp', axis=1, inplace=True)
        std_trace['timestamp'] = fixed_timestamps

        cols = std_trace.columns.tolist()

        cols.insert(1, cols[-1])
        cols.pop(-1)

        std_trace = std_trace[cols]
            
        print('Timestamps fixed!\n')

        return std_trace