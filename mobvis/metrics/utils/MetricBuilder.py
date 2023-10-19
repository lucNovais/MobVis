from mobvis.metrics.spatial.TravelDistance import TravelDistance
from mobvis.metrics.spatial.RadiusOfGyration import RadiusOfGyration
from mobvis.metrics.spatial.VisitOrder import VisitOrder
from mobvis.metrics.temporal.VisitTime import VisitTime
from mobvis.metrics.temporal.TravelTime import TravelTime
from mobvis.metrics.social.IntercontactTime import IntercontactTime

class MetricBuilder:
    """Factory pattern to create metrics based on user request.
    """

    @staticmethod
    def build_metric(metric, **kwargs):
        """Method that builds a metric with specific parameters.

        Parameters:

        `metric` (str): String that corresponds to the metric.
        `kwargs`: Specific parameters that vary by metric. See individual docstrings for more details.

            - Travel Distance (TRVD): trace_loc, dist_type
            - Radius of Gyration (RADG): trace, trace_loc, sl_centers, homes, dist_type
            - Visit Order (VISO): trace_loc
            - Visit Time (VIST): trace_loc
            - Travel Time (TRVT): trace_loc
            - Intercontact Time (INCO): contacts_df

        Returns:

        `IMetric` child class that corresponds to the specified metric. 
        """
        if metric == 'TRVD':
            return TravelDistance(
                trace_name=kwargs.get('trace_name'),
                trace_loc=kwargs.get('trace_loc'),
                dist_type=kwargs.get('dist_type'),
                logger=kwargs.get('logger')
            )
        if metric == 'RADG':
            return RadiusOfGyration(
                trace_name=kwargs.get('trace_name'),
                trace=kwargs.get('trace'),
                trace_loc=kwargs.get('trace_loc'),
                sl_centers=kwargs.get('sl_centers'),
                homes=kwargs.get('homes'),
                dist_type=kwargs.get('dist_type'),
                logger=kwargs.get('logger')
            )
        if metric == 'VISO':
            return VisitOrder(
                trace_name=kwargs.get('trace_name'),
                trace_loc=kwargs.get('trace_loc'),
                logger=kwargs.get('logger')
            )
        if metric == 'VIST':
            return VisitTime(
                trace_name=kwargs.get('trace_name'),
                trace_loc=kwargs.get('trace_loc'),
                logger=kwargs.get('logger')
            )
        if metric == 'TRVT':
            return TravelTime(
                trace_name=kwargs.get('trace_name'),
                trace_loc=kwargs.get('trace_loc'),
                logger=kwargs.get('logger')
            )
        if metric == 'INCO':
            return IntercontactTime(
                trace_name=kwargs.get('trace_name'),
                contacts_df=kwargs.get('contacts_df'),
                logger=kwargs.get('logger')
            )
