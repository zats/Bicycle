__author__ = 'zats'


import io
import csv
from datetime import datetime
from flask.ext.compress import Compress
from flask.ext.sqlalchemy import *
from flask import Flask, request, flash, url_for, redirect, render_template, abort, jsonify
from random import randint
import urllib.request
from sqlalchemy import asc
from wsgi.scrapers import *


CRON_INTERVAL = 2
SERVICES = {
    'telofun': {'class': 'Telofun'},
    'bayareabikeshare': {'class': 'BayAreaBikeShare'},
    'bikesharetoronto': {'class': 'BikeShareToronto'},
    'citibikenyc': {'class': 'CityBikeNewYork'},
    'divvybikes': {'class': 'DivvyBikes'}
}

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
app.config.update(
    JSONIFY_PRETTYPRINT_REGULAR=False,
    JSON_SORT_KEYS=False
)
db = SQLAlchemy(app)


class Station(db.Model):
    __tablename__ = 'stations'
    id = db.Column('id', db.Integer, primary_key=True)
    service = db.Column(db.String)
    station_id = db.Column(db.String)
    address = db.Column(db.String)
    description = db.Column(db.String)
    available_bicycles = db.Column(db.Integer)
    available_docks = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean)

    def __init__(self, service, dictionary):
        expected_keys = ['station_id', 'address', 'description',
                         'latitude', 'longitude',
                         'available_bicycles', 'available_docks', 'capacity',
                         'is_active']
        for key in expected_keys:
            setattr(self, key, dictionary[key])
        self.service = service
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        pass

    def update(self, dictionary):
        expected_keys = ['address', 'description',
                         'latitude', 'longitude',
                         'available_bicycles', 'available_docks', 'capacity',
                         'is_active']
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
            'available_docks': self.available_docks,
            'capacity': self.capacity,
            'created_at': self.created_at.timestamp(),
            'updated_at': self.updated_at.timestamp(),
            'is_active': self.is_active
        }


class StationInfo(db.Model):
    __tablename__ = 'station_infos'
    id = db.Column('id', db.Integer, primary_key=True)
    service = db.Column(db.String)
    station_id = db.Column(db.String)
    available_bicycles = db.Column(db.Float)
    available_docks = db.Column(db.Float)
    samples_count = db.Column(db.Integer)
    hour_of_week = db.Column(db.Float)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, service, dictionary, hour_of_week):
        self.service = service
        self.station_id = dictionary['station_id']
        self.available_bicycles = dictionary['available_bicycles']
        self.available_docks = dictionary['available_docks']
        self.hour_of_week = hour_of_week
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.samples_count = 1
        pass

    def update(self, dictionary):
        self.samples_count += 1
        self.available_bicycles += (dictionary['available_bicycles'] - self.available_bicycles) / float(
            self.samples_count)
        self.available_docks += (dictionary['available_docks'] - self.available_docks) / float(self.samples_count)
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            'available_bicycles': self.available_bicycles,
            'available_docks': self.available_docks,
            'hour_of_week': self.hour_of_week
        }


@app.route("/")
def hello():
    return "<h1 style='text-align: center;'>🐮🐶 Moof!</h1>"


@app.route("/ping")
def ping():
    response = urllib.request.urlopen('http://pingpong-zats.rhcloud.com/')
    print("Ping recevied. Pong.\n%s" % response)

@app.route("/db/setup")
def setup_db():
    try:
        db.drop_all()
        db.create_all()
    except Exception as e:
        return error_response(500, str(e))
    return "Success"


@app.route("/db/test")
def test_db():
    b1 = randint(0, 20)
    b2 = randint(0, 15)
    dictionary = {
        'telofun::1': {'station_id': 'telofun::1', 'address': 'King George 12',
                       'description': 'To the right from the booth', 'latitude': 33.423, 'longitude': 44.235,
                       'available_bicycles': b1, 'available_docks': 20 - b1, 'capacity': 20, 'is_active': False},
        'telofun::2': {'station_id': 'telofun::2', 'address': 'Wall street, 31', 'description': 'Next to the fountain',
                       'latitude': 33.123, 'longitude': 44.241,
                       'available_bicycles': b2, 'available_docks': 15 - b2, 'capacity': 15, 'is_active': True}
    }
    try:
        result = update_with_dictionary('telofun', dictionary)
    except Exception as e:
        return error_response(500, str(e))

    return result


@app.route("/api/1/<service>/scrape")
def scrape_for_service(service, swallaw_exceptions=True):
    if service not in SERVICES:
        return error_response(404, "Service \"" + service + "\" is not found")

    service_object = SERVICES[service]
    try:
        service_class = eval(service_object['class'] + 'Scraper')
        scraper = service_class()
        markers = scraper.scrape(scraper.service_url())
        update_with_dictionary(service, markers)
    except Exception as e:
        if swallaw_exceptions:
            return error_response(500, str(e))
        else:
            raise e

    return "Success"


@app.route("/api/1/<service>/stations")
def fetch_stations_for_service(service):
    if service not in SERVICES:
        abort(404)

    stations = Station.query.filter(Station.service == service).order_by(asc(Station.station_id))
    result = {'stations': []}
    for station in stations:
        result['stations'].append(station.to_dict())

    return jsonify(result)


@app.route("/api/1/<service>/statistics")
def fetch_statistics(service):
    try:
        station_ids = request.args['station_ids']
        time_ranges = request.args['time_ranges']
    except Exception as e:
        return error_response(400, "Invalid parameters. " + str(e))

    time_ranges = array_from_parameter(time_ranges)
    station_ids = array_from_parameter(station_ids)

    query = StationInfo.query.filter(StationInfo.service == service,
                                     StationInfo.station_id.in_(station_ids))
    for time_range in time_ranges:
        to_int = lambda x: int(x)
        arr = list(map(to_int, time_range.rsplit('-')))
        query = query.filter(StationInfo.hour_of_week.between(arr[0], arr[1]))

    query = query.order_by(asc(StationInfo.hour_of_week))

    outputs = {}
    for station_info in query:
        station_id = station_info.station_id
        if station_id not in outputs:
            output = io.StringIO()
            outputs[station_id] = output
            writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(list(station_info.to_dict().keys()))
            writer.writerow(list(station_info.to_dict().values()))
        else:
            writer.writerow(list(station_info.to_dict().values()))
    outputs = {key: value.getvalue() for (key, value) in outputs.items()}
    return jsonify({'response': {
        'statistics': [{
            'service': service,
            'stations': outputs
        }]
    }})


def update_with_dictionary(service, dictionary):
    station_ids = dictionary.keys()
    hour_of_week = current_hour_of_week()

    # Station
    dictionary_copy = dictionary.copy()
    fetched_stations = Station.query.filter(Station.station_id.in_(station_ids),
                                            Station.service == service)

    # Update existent
    for station in fetched_stations:
        station_dictionary = dictionary_copy[station.station_id]
        station.update(station_dictionary)
        del dictionary_copy[station.station_id]

    # Create
    for station_id, station_dictionary in dictionary_copy.items():
        station = Station(service, station_dictionary)
        db.session.add(station)

    # Station info
    dictionary_copy = dictionary.copy()
    fetched_station_infos = StationInfo.query.filter(StationInfo.station_id.in_(station_ids),
                                                     StationInfo.service == service,
                                                     StationInfo.hour_of_week == hour_of_week)

    # Update existent
    for station_info in fetched_station_infos:
        station_dictionary = dictionary_copy[station_info.station_id]
        station_info.update(station_dictionary)
        del dictionary_copy[station_info.station_id]

    # Create
    for station_id, station_dictionary in dictionary_copy.items():
        station_info = StationInfo(service, station_dictionary, hour_of_week)
        db.session.add(station_info)

    db.session.commit()
    return 'Great success'


def current_hour_of_week():
    now = time.gmtime(time.time())
    hour_of_week = now.tm_wday * 24 + round((now.tm_hour + now.tm_min / 60) * 1000) / 1000
    return hour_of_week


def error_response(code, message):
    response = jsonify({'code': code, 'error': message})
    response.status_code = code
    return response


def array_from_parameter(string):
    if not string.startswith('[') or not string.endswith(']'):
        return None
    string = string[1:-1]
    return string.rsplit(',')


if __name__ == "__main__":
    app.run()

