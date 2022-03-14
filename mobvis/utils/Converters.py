import pandas as pd
from dateutil.parser import parse

def convert_datetime(df):
    """Converts any datetime format to timestamps in seconds.

    Params
    ------

    df: TrajDataFrame already pre-processed from the parser module.

    Return
    ------

    ts_df: TrajDataFrame with timestamps instead of datetimes.
    start_date: The initial datetime of the trajectory.
    """

    # df.datetime = parse(df['datetime'].tolist())
    for string in df.datetime.tolist():
        print(parse(str(string)))

    start_date = df.datetime[0]

    seconds = (df.datetime - start_date).values.view('<i8')/10**9

    ts_df = df
    del df
    ts_df.datetime = seconds

    return [ts_df, start_date]


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