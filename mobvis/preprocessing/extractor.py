import pandas as pd

from mobvis.metrics.spatial.TravelDistance import TravelDistance
from mobvis.metrics.spatial.RadiusOfGyration import RadiusOfGyration

def extract(metric, filename, trace, df_type, **kwargs):
    if kwargs.get('max_d'):
        max_d = float(kwargs.get('max_d'))
    else:
        max_d = 30

    if kwargs.get('pause_t'):
        pause_t = float(kwargs.get('pause_t'))
    else:
        pause_t = 5

    if metric == 'TRVD':
        trvd = TravelDistance(filename=filename, max_d=max_d, pause_threshold=pause_t, trace=trace, df_type=df_type)
        [trvd_df, trace_loc, sl_centers, nodes_stlc] = trvd.extract()

        return [trvd_df, trace_loc, sl_centers, nodes_stlc]

    if metric == 'RADG':
        radg = RadiusOfGyration(filename=filename, max_d=max_d, pause_threshold=pause_t, trace=trace, df_type=df_type)
        [trace_radg, homes] = radg.extract()

        return [trace_radg, homes]