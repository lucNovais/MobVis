from mobvis.metrics.spatial.TravelDistance import TravelDistance
from mobvis.metrics.spatial.RadiusOfGyration import RadiusOfGyration
from mobvis.metrics.spatial.VisitOrder import VisitOrder
from mobvis.metrics.temporal.VisitTime import VisitTime
from mobvis.metrics.temporal.TravelTime import TravelTime
from mobvis.metrics.social.IntercontactTime import IntercontactTime

from multiprocessing import Process
from multiprocessing import Manager

class MultiMetricExtractor:
    def __init__(self):
        pass

    @classmethod
    def multiextractor(cls, metric, **kwargs):
        manager = Manager()
        return_dict = manager.dict()
        if metric == 'TRVD':
            traces_locs = kwargs.get('traces_locs')
            dist_types = kwargs.get('dist_types')
            
            trvds = []

            for i in range(len(traces_locs)):
                trvds.append(TravelDistance(trace_loc=traces_locs[i], dist_type=dist_types[i]))
            
            processes = []
            for i, trvd in enumerate(trvds):
                keywordargs = {
                    'proc_num': i
                    , 'return_dict': return_dict
                }
                processes.append(Process(target=trvd.extract, kwargs=keywordargs))

            for process in processes:
                process.start()
            
            for process in processes:
                process.join()

            return return_dict.values()

        elif metric == 'RADG':
            traces = kwargs.get('traces')
            traces_locs = kwargs.get('traces_locs')
            sls_centers = kwargs.get('sls_centers')
            homes = kwargs.get('homes')
            dist_types = kwargs.get('dist_types')

            radgs = []

            for i in range(len(traces)):
                radgs.append(RadiusOfGyration(trace=traces[i]
                    , trace_loc=traces_locs[i]
                    , sl_centers=sls_centers[i]
                    , homes=homes[i]
                    , dist_type=dist_types[i]
                ))
            
            processes = []
            for i, radg in enumerate(radgs):
                keywordargs = {
                    'proc_num': i
                    , 'return_dict': return_dict
                }
                processes.append(Process(target=radg.extract, kwargs=keywordargs))

            for process in processes:
                process.start()
            
            for process in processes:
                process.join()
            
            return return_dict.values()

        elif metric == 'VISO':
            traces_locs = kwargs.get('traces_locs')

            visos = []

            for i in range(len(traces_locs)):
                visos.append(VisitOrder(trace_loc=traces_locs[i]))
            
            processes = []
            for i, viso in enumerate(visos):
                keywordargs = {
                    'proc_num': i
                    , 'return_dict': return_dict
                }
                processes.append(Process(target=viso.extract, kwargs=keywordargs))

            for process in processes:
                process.start()
            
            for process in processes:
                process.join()
            
            return return_dict.values()

        elif metric == 'TRVT':
            traces_locs = kwargs.get('traces_locs')

            trvts = []

            for i in range(len(traces_locs)):
                trvts.append(TravelTime(trace_loc=traces_locs[i]))
            
            processes = []
            for i, trvt in enumerate(trvts):
                keywordargs = {
                    'proc_num': i
                    , 'return_dict': return_dict
                }
                processes.append(Process(target=trvt.extract, kwargs=keywordargs))

            for process in processes:
                process.start()
            
            for process in processes:
                process.join()           

            return return_dict.values()

        elif metric == 'VIST':
            traces_locs = kwargs.get('traces_locs')

            vists = []

            for i in range(len(traces_locs)):
                vists.append(VisitTime(trace_loc=traces_locs[i]))
            
            processes = []
            for i, vist in enumerate(vists):
                keywordargs = {
                    'proc_num': i
                    , 'return_dict': return_dict
                }
                processes.append(Process(target=vist.extract, kwargs=keywordargs))

            for process in processes:
                process.start()
            
            for process in processes:
                process.join()           

            return return_dict.values()
