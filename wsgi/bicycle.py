from datetime import datetime
from flask.ext.sqlalchemy import *
from flask import Flask, request, flash, url_for, redirect, render_template, abort
import time


CRON_INTERVAL = 2


app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app)


class Station(db.Model):
    __tablename__ = 'stations'
    id = db.Column('station_id', db.String, primary_key=True)
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
        expected_keys = ['id', 'address', 'description', 'latitude', 'longitude', 'available_bicycles',
                         'available_poles', 'capacity']
        for key in expected_keys:
            setattr(self, key, dictionary[key])
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def update_with_dictionary(self, dictionary):
        expected_keys = ['address', 'description', 'latitude', 'longitude', 'available_bicycles', 'available_poles',
                         'capacity']
        did_update = False
        for key in expected_keys:
            if (key in dictionary) and (getattr(self, key, None) != dictionary[key]):
                setattr(self, key, dictionary[key])
                did_update = True
        if did_update:
            self.updated_at = datetime.utcnow()
        return did_update


class StationInfo(db.Model):
    __tablename__ = 'station_infos'
    id = db.Column('station_id', db.String, primary_key=True)
    available_bicycles = db.Column(db.Integer)
    available_poles = db.Column(db.Integer)
    samples_count = db.Column(db.Integer)
    hour_of_week = db.Column(db.Float)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, dictionary):
        expected_keys = ['id', 'available_bicycles', 'available_poles', 'samples_count', 'hour_of_week']
        for key in expected_keys:
            setattr(self, key, dictionary[key])
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def update_with_dictionary(self, dictionary):
        expected_keys = ['available_bicycles', 'available_poles', 'samples_count', 'hour_of_week']
        did_update = False
        for key in expected_keys:
            if (key in dictionary) and (getattr(self, key, None) != dictionary[key]):
                setattr(self, key, dictionary[key])
                did_update = True
        if did_update:
            self.updated_at = datetime.utcnow()
        return did_update


@app.route("/")
@app.route("/hello")
def hello():
    return "Hello World!"


@app.route("/new")
def new():
    dictionary = {
        'telofun::1': {'id': 'telofun::1', 'address': 'King George 12',
                       'description': 'To the right from the falafel booth', 'latitude': 33.423, 'longitude': 44.235,
                       'available_bicycles': 12, 'available_poles': 7, 'capacity': 20},
        'telofun::2': {'id': 'telofun::2', 'address': 'Dizengoff 31', 'description': 'Next to the fountain',
                       'latitude': 33.123, 'longitude': 44.241, 'available_bicycles': 10, 'available_poles': 5,
                       'capacity': 15}
    }
    update_with_dictionary(dictionary)
    return redirect(url_for('hello'))


def update_with_dictionary(dictionary):
    station_ids = dictionary.keys()
    hour_of_week = current_hour_of_week()

    # Station
    dictionary_copy = dictionary.copy()
    fetched_stations = Station.query.filter(Station.id.in_(station_ids))

    # Update existent
    for station in fetched_stations:
        station_dictionary = dictionary_copy[station.id];
        station.update_with_dictionary(station_dictionary)
        del dictionary_copy[station.id]

    # Create
    for station_id, station_dictionary in dictionary_copy:
        station = Station(station_dictionary)
        db.session.add(station)

    # Station info
    dictionary_copy = dictionary.copy()
    fetched_station_infos = StationInfo.query(StationInfo).filter(StationInfo.id.in_(station_ids),
                                                                  StationInfo.hour_of_week == hour_of_week)

    # Update existent
    for station_info in fetched_station_infos:
        station_dictionary = dictionary_copy[station.id];
        station_info.update_with_dictionary(station_dictionary)
        del dictionary_copy[station.id]

    # Create
    for station_id, station_dictionary in dictionary_copy:
        station_info = StationInfo(station_dictionary)
        db.session.add(station_info)

    db.session.commit()


def current_hour_of_week():
    now = time.gmtime(time.time())
    hour_of_week = round((now.tm_wday * 24 * 60 * 60 +
                          now.tm_hour * 60 * 60 +
                          (now.tm_min / CRON_INTERVAL) * CRON_INTERVAL) / (60.0 * 60.0), 3)
    return hour_of_week


if __name__ == "__main__":
    app.run(debug=True)

