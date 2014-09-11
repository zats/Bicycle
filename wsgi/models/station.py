__author__ = 'zats'


from datetime import datetime
from wsgi.bicycle import db


class Station(db.Model):
    __tablename__ = 'stations'
    id = db.Column('id', db.Integer, primary_key=True)
    station_id = db.Column(db.String)
    address = db.Column(db.String)
    description = db.Column(db.String)
    available_bicycles = db.Column(db.Integer)
    available_poles = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, dictionary):
        expected_keys = ['station_id', 'address', 'description',
                         'latitude', 'longitude',
                         'available_bicycles', 'available_poles', 'capacity']
        for key in expected_keys:
            setattr(self, key, dictionary[key])
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        pass

    def update_with_dictionary(self, dictionary):
        expected_keys = ['address', 'description',
                         'latitude', 'longitude',
                         'available_bicycles', 'available_poles','capacity']
        did_update = False
        for key in expected_keys:
            if (key in dictionary) and (getattr(self, key, None) != dictionary[key]):
                setattr(self, key, dictionary[key])
                did_update = True
        if did_update:
            self.updated_at = datetime.utcnow()
        return did_update

    def to_dict(self):
        return {
            'id': self.station_id,
            'address': self.address,
            'description': self.description,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'available_bicycles': self.available_bicycles,
            'available_poles': self.available_poles,
            'capacity': self.capacity,
            'created_at': self.created_at.timestamp(),
            'updated_at': self.updated_at.timestamp()
        }
