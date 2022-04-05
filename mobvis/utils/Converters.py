import pandas as pd
from dateutil.parser import parse

def convert_datetime(trace, date_column):
    """Converts any datetime format to timestamps in seconds. The first datetime will be considered as the 0 time.

    Parameters:

    `trace` (pandas.DataFrame): DataFrame of the trace.
    `date_column` (str): Name of the date column on the DataFrame.

    Returns:

    `trace` (pandas.DataFrame): DataFrame with the datetimes converted to seconds.
    """

    trace[date_column] = pd.to_datetime(trace[date_column])
    first_timestamp = trace[date_column].min()
    
    new_timestamps = []
    
    for i, row in trace.iterrows():
        current_timestamp = row[date_column]
        difference = (current_timestamp - first_timestamp).total_seconds()
        
        new_timestamps.append(difference)
        
    trace = trace.drop(date_column, axis=1)
    trace[date_column] = new_timestamps
    
    return trace


# def filter_datetime(df):
#     ts = []
#     yr = pd.to_datetime(df.timestamp.values).year
#     mnth = pd.to_datetime(df.timestamp.values).month
#     day = pd.to_datetime(df.timestamp.values).day
#     hr = pd.to_datetime(df.timestamp.values).hour
#     mnt = pd.to_datetime(df.timestamp.values).minute
#     sec = pd.to_datetime(df.timestamp.values).second
    
#     for years, months, days, hours, minutes, seconds in zip(yr, mnth, day, hr, mnt, sec):
#         aux = '{:02d}'.format(years) + '-{:02d}'.format(months) + '-{:02d}'.format(days) + ' {:02d}'.format(hours) + ':{:02d}'.format(minutes) + ':{:02d}'.format(seconds)
#         ts.append(aux)

#     return ts