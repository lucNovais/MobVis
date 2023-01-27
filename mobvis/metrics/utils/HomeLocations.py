import pandas as pd

from concurrent.futures import ThreadPoolExecutor

from mobvis.utils import Timer

class HomeLocations:
    """Class that contains the method for finding the Home Locations of a given set of
       nodes and Geo-locations.
    """
    def __init__(self):
        pass

    @classmethod
    def multifinder_homes(cls, trace_locations):
        print('Finding home locations for multiple traces:\n')

        homes = []

        with ThreadPoolExecutor() as executor:
            for result in executor.map(cls.find_homes, trace_locations):
                homes.append(result)
        
        return homes

    @classmethod
    @Timer.timed
    def find_homes(cls, trace_loc):
        """Finds the Home-locations of all the nodes of a trace.
        
        Params:

        `trace_loc` (pandas.DataFrame): Geo-locations DataFrame of the trace extracted by the mobvis.metrics.utils.Locations module.
        
        Returns:

        `homes` (pandas.DataFrame): Home-locations of each node.
            - id: Node identifier
            - home_location: Geo-location that is considered the node Home-location
            - x: x coordinate of the location
            - y: y coordinate of the location
        """
        print('Finding the Home Locations...')

        homes = pd.DataFrame(columns=['id', 'home_location', 'x', 'y'])
        prev_row = trace_loc.iloc[0]
        longer_stay_time = 0
        stay_time = 0
        current_home = trace_loc.iloc[0]
        
        for index, row in trace_loc.iloc[1:].iterrows():
            if row.id == prev_row.id:
                if row.sl == prev_row.sl:
                    stay_time += (row.timestamp - prev_row.timestamp)
                else:
                    if stay_time > longer_stay_time:
                        longer_stay_time = stay_time
                        current_home = prev_row
                    
                    stay_time = 0
            else:
                new_row = pd.DataFrame({
                    'id': [prev_row.id],
                    'home_location': [current_home.sl],
                    'x': [current_home.x],
                    'y': [current_home.y]
                })
                homes = pd.concat([homes, new_row], ignore_index=True)
                
                current_home = row
                stay_time = 0
                longer_stay_time = 0
                
            prev_row = row

        new_row = pd.DataFrame({
            'id': [prev_row.id],
            'home_location': [current_home.sl],
            'x': [current_home.x],
            'y': [current_home.y]
        })
        homes = pd.concat([homes, new_row], ignore_index=True)
        
        print('Home locations found!')
        return homes