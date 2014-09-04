from datetime import datetime
import logging
from flask.ext.sqlalchemy import *
from flask import Flask, request, flash, url_for, redirect, render_template, abort, jsonify
import time
from random import randint

CRON_INTERVAL = 2

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app)


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
            'created_at': self.created_at.time(),
            'updated_at': self.updated_at.time()
        }


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


@app.route("/")
@app.route("/hello")
def hello():
    return "Hello World!"


@app.route("/new")
def new():
    b1 = randint(0, 20)
    b2 = randint(0, 15)
    dictionary = {
        'telofun::1': {'station_id': 'telofun::1', 'address': 'King George 12',
                       'description': 'To the right from the falafel booth', 'latitude': 33.423, 'longitude': 44.235,
                       'available_bicycles': b1, 'available_poles': 20 - b1, 'capacity': 20},
        'telofun::2': {'station_id': 'telofun::2', 'address': 'Dizengoff 31', 'description': 'Next to the fountain',
                       'latitude': 33.123, 'longitude': 44.241,
                       'available_bicycles': b2, 'available_poles': 15 - b2, 'capacity': 15}
    }
    return update_with_dictionary(dictionary)


@app.route("/api/1/stations/<service>")
def fetch_all_stations(service):
    response = []
    for station in Station.query.filter(Station.station_id.startswith(service)):
        response.append(station.to_dict())
    return jsonify(stations=response)


def update_with_dictionary(dictionary):
    logging.info('Hello')

    station_ids = dictionary.keys()
    hour_of_week = current_hour_of_week()

    # Station
    dictionary_copy = dictionary.copy()
    fetched_stations = Station.query.filter(Station.station_id.in_(station_ids))

    # Update existent
    for station in fetched_stations:
        station_dictionary = dictionary_copy[station.station_id];
        station.update_with_dictionary(station_dictionary)
        logging.info('updating station for \"' + station.station_id + '\"')
        # db.session.add(station)
        del dictionary_copy[station.station_id]

    # Create
    for station_id, station_dictionary in dictionary_copy.items():
        station = Station(station_dictionary)
        logging.info('creating station for \"' + station_id + '\"')
        db.session.add(station)

    # Station info
    dictionary_copy = dictionary.copy()
    fetched_station_infos = StationInfo.query.filter(StationInfo.station_id.in_(station_ids),
                                                     StationInfo.hour_of_week == hour_of_week)

    # Update existent
    for station_info in fetched_station_infos:
        station_dictionary = dictionary_copy[station_info.station_id]
        station_info.update_with_dictionary(station_dictionary)
        logging.info('updating station info for \"' + station_info.station_id + '\"')
        # db.session.add(station_info)
        del dictionary_copy[station_info.station_id]

    # Create
    for station_id, station_dictionary in dictionary_copy.items():
        station_info = StationInfo(station_dictionary, hour_of_week)
        logging.info('creating station info for \"' + station_id + '\"')
        db.session.add(station_info)

    db.session.commit()
    return 'Great success'


def current_hour_of_week():
    now = time.gmtime(time.time())
    hour_of_week = round((now.tm_wday * 24 * 60 * 60 +
                          now.tm_hour * 60 * 60 +
                          (now.tm_min / CRON_INTERVAL) * CRON_INTERVAL) / (60.0 * 60.0), 3)
    return hour_of_week


if __name__ == "__main__":
    app.run()

