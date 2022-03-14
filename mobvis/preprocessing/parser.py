import pandas as pd

from mobvis.utils import Timer
from mobvis.utils import Converters

SUPPORTED_TIMESTAMPS = [
    'datetime',
    'date',
    'time'
]

SUPPORTED_COORDINATES = [
    'lat',
    'lng',
    'long',
    'latitude',
    'longitude'
]


pd.set_option('display.precision', 10)

class Parser:
    def __init__(self):
        pass

    @classmethod
    @Timer.timed
    def parse(cls, raw_trace, raw_trace_cols, is_ordered):
        """Method that converts the given DataFrame to the MobVis standard format.

        Parameters:

        `raw_trace` (pandas.DataFrame): Raw DataFrame containing the original trace.
        `raw_trace_cols` (str[]): Array containing the names of the raw trace columns in order.
        `is_ordered` (bool): 'True' if the rows of the raw DataFrame are ordered by the id and timestamps, `False` otherwise.

        Returns:

        `std_trace` (pandas.DataFrame): DataFrame corresponding to the parsed trace.
        """
        print('Parsing the given DataFrame...')

        if raw_trace.columns.size == 1:
            raw_trace[raw_trace_cols] = raw_trace[raw_trace.columns[0]].str.split(' ', expand=True)
            raw_trace.drop(raw_trace.columns[0], axis=1, inplace=True)
        else:
            raw_trace.rename(columns={
                0: raw_trace_cols[0],
                1: raw_trace_cols[1],
                2: raw_trace_cols[2],
                3: raw_trace_cols[3]
            }, inplace=True)

        initial_id = int(raw_trace.id[0])

        std_trace = cls.check_columns(raw_trace, raw_trace_cols)
        std_trace = cls.fix_timestamps(std_trace, initial_id)

        if not is_ordered:
            std_trace = cls.order_rows(std_trace)

        print('Successfully parsed!\n')
        print(std_trace)

        return std_trace

    def check_columns(raw_trace, raw_trace_cols):
        """Detects the columns informed for the raw trace and performs the procedures to convert
           them to the standard MobVis format.
        """
        default_order = ['id', 'timestamp', 'x', 'y']

        # Check if the timestamps column in the raw trace are on the datetime format, and consider some
        # possible names on the SUPPORTED_TIMESTAMPS array (case insensitive).
        raw_timestamp = [item for item in raw_trace_cols if item.lower() in SUPPORTED_TIMESTAMPS]
        if raw_timestamp:
            if raw_timestamp != 'time':
                raw_trace = Converters.convert_datetime(raw_trace)
            raw_trace.rename(columns={raw_timestamp: 'timestamp'}, inplace=True)

        # Check if the coordinates column in the raw trace are on the lat/long format, and consider some
        # possible names on the SUPPORTED_COORDINATES array (case insensitive).
        raw_coord = [item for item in raw_trace_cols if item.lower() in SUPPORTED_COORDINATES]
        if raw_coord:
            raw_trace.rename(columns={raw_coord[0]: 'y', raw_coord[1]: 'x'}, inplace=True)
            for i, col in enumerate(raw_trace_cols):
                if col == raw_coord[0]:
                    raw_trace_cols[i] = 'y'
                if col == raw_coord[1]:
                    raw_trace_cols[i] = 'x'

        # Sorts the dataframe columns according to the default library order
        std_trace_cols = [item for x in default_order for item in raw_trace_cols if item == x]
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
    def fix_timestamps(cls, std_trace, initial_id):
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

        first_timestamp = std_trace.loc[std_trace.id == initial_id].timestamp.values[0]
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