import logging
from flask.ext.sqlalchemy import *
from flask import Flask, request, flash, url_for, redirect, render_template, abort, jsonify
from random import randint
from wsgi.models.station import Station
from wsgi.scrapers.telofun_scraper import TelofunScraper
from wsgi.models.station_info import StationInfo


CRON_INTERVAL = 2

SERVICES = {'telofun': TelofunScraper.__class__}

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app)


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


@app.route("/api/1/scrapers/<service>")
def fetch_all_stations(service):
    if service not in SERVICES:
        return "<h1>Unknown service</h1>"

    service_class = SERVICES[service]
    scraper = service_class()
    markers = scraper.scrape(scraper.service_url())
    try:
        update_with_dictionary(markers)
    except:
        return "Failed"

    return "Success"


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

