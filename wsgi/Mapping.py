__author__ = 'zats'


class CoordinateRegion(object):

    def __init__(self, min_latitude, min_longitude, max_latitude, max_longitude):
        self.min_latitude = min_latitude
        self.min_longitude = min_longitude
        self.max_latitude = max_latitude
        self.max_longitude = max_longitude
