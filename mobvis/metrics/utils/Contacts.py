import pandas as pd

from itertools import combinations
from mobvis.utils import Timer

from mobvis.utils.Utils import haversine
from scipy.spatial import distance

pd.set_option('display.precision', 10)

class Contacts:
    """Contains the methods for finding the contacts between the trace nodes.
    """
    def __init__(self):
        pass

    def euclidean_contact_detection(df, radius):
        """Apply the contact detection on all pairs of the trace by using the Euclidean formula.
        """
        edges = []
        raw_data_matrix = df.values
        
        for row1, row2 in combinations(raw_data_matrix, 2):
            lat1 = row1[3]
            lon1 = row1[2]
            lat2 = row2[3]
            lon2 = row2[2]
            dist = distance.euclidean((lat1, lon1), (lat2, lon2))

            if dist <= radius:
                if row1[0] != row2[0]:
                    edges.append((row1[0], row2[0], lat1, lon1, lat2, lon2, row1[1]))

        contacts_df = pd.DataFrame(edges, columns=['id1', 'id2', 'x1', 'y1', 'x2', 'y2', 'timestamp'])

        return contacts_df

    def haversine_contact_detection(df, radius):
        """Apply the contact detection on all pairs of the trace by using the Haversine formula.
        """
        edges = []
        raw_data_matrix = df.values
        
        for row1, row2 in combinations(raw_data_matrix, 2):
            lat1 = row1[3]
            lon1 = row1[2]
            lat2 = row2[3]
            lon2 = row2[2]
            dist = haversine(lat1, lon1, lat2, lon2)

            if dist <= radius:
                if row1[0] != row2[0]:
                    edges.append((row1[0], row2[0], lat1, lon1, lat2, lon2, row1[1]))

        contacts_df = pd.DataFrame(edges, columns=['id1', 'id2', 'x1', 'y1', 'x2', 'y2', 'timestamp'])

        return contacts_df

    @classmethod
    @Timer.timed
    def detect_contacts(cls, df, radius, dist_type):
        """Detects contacts between each pair of nodes on the trace.

        Params:
        
        `df` (pandas.DataFrame): DataFrame corresponding to the parsed trace.
        `radius` (float): Contact radius of the nodes.
        `dist_type` (str): Distance formula. Supported types are: Haversine and Euclidean.

        Returns:

        `contacts` (pandas.DataFrame): DataFrame containing all the contacts of the trace.
            - id1: First node identifier
            - id2: Second node identifier
            - x1: x coordinate of the first node
            - y1: y coordinate of the first node
            - x2: x coordinate of the second node
            - y2: y coordinate of the second node
        """

        print('Detecting the contacts between the nodes...')
        print(f'\nParameters:\nContact Radius: {radius}\nDistance Formula: {dist_type}')

        timestamps = df.timestamp.unique()
        contacts = pd.DataFrame(columns=['id1', 'id2', 'x1', 'y1', 'x2', 'y2'])

        if dist_type.lower() == 'haversine':
            for t in timestamps:
                filtered_df = df.loc[df.timestamp == t]
                contacts = pd.concat([contacts, cls.haversine_contact_detection(filtered_df, radius)], ignore_index=True)
        elif dist_type.lower() == 'euclidean':
            for t in timestamps:
                filtered_df = df.loc[df.timestamp == t]
                contacts = pd.concat([contacts, cls.euclidean_contact_detection(filtered_df, radius)], ignore_index=True)
                    

        print('Contacts Detected!')
            
        print(contacts.head())
        print(f'Number of contacts: {len(contacts)}')

        return contacts