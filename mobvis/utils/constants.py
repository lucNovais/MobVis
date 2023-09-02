""" The purpose of this module is to store constants that will be used several
    times throughout MobVis.
"""

# This list presents all the timestamp column names supported by MobVis, that is,
# the input trace must have a timestamp (or date) column with one of the names
# in this list.
SUPPORTED_TIMESTAMPS = [
    't',
    'datetime',
    'date',
    'time',
    'gps_time'
]

# This list presents all the coordinate column names supported by MobVis, following
# the same logic as the list mentioned above.
SUPPORTED_COORDINATES = [
    'lat',
    'lng',
    'long',
    'latitude',
    'longitude'
]

# This list presents all the identifier column names supported by MobVis.
SUPPORTED_IDENTIFIERS = [
    'i',
    'id',
    'identifier',
    'uid',
    'node_id'
]
