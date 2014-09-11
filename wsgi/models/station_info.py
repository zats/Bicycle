__author__ = 'zats'


from datetime import datetime
from wsgi.bicycle import db


class StationInfo(db.Model):
    __tablename__ = 'station_infos'
    id = db.Column('id', db.Integer, primary_key=True)
    station_id = db.Column(db.String)
    available_bicycles = db.Column(db.Float)
    available_poles = db.Column(db.Float)
    samples_count = db.Column(db.Integer)
    hour_of_week = db.Column(db.Float)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, dictionary, hour_of_week):
        self.station_id = dictionary['station_id']
        self.available_bicycles = dictionary['available_bicycles']
        self.available_poles = dictionary['available_poles']
        self.hour_of_week = hour_of_week
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.samples_count = 1
        pass

    def update_with_dictionary(self, dictionary):
        self.samples_count += 1
        self.available_bicycles += (dictionary['available_bicycles'] - self.available_bicycles) / float(
            self.samples_count)
        self.available_poles += (dictionary['available_poles'] - self.available_poles) / float(self.samples_count)
        self.updated_at = datetime.utcnow()
