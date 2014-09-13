import json

__author__ = 'zats'


import re
from bs4 import BeautifulSoup
from wsgi.custom_exceptions import ParsingErrorException
from wsgi.scrapers.base_scraper import BaseScraper


class BayAreaBikeShareScraper(BaseScraper):
    def service_name(self):
        return 'bayareabikeshare'

    def service_url(self):
        return 'http://www.bayareabikeshare.com/stations/json'

    def scrape(self, url):
        json_data = self.open_url(url)
        data = json.load(json_data)

        result = {}
        for raw_station in data['stationBeanList']:
            station_id, marker = self.parse_station(raw_station)
            result[station_id] = marker
        return result

    def parse_stations(self, raw_station):
        address = self.parse_address(raw_station)
        station_id = str(raw_station['id'])
        station = {
            'station_id': station_id,
            'latitude': raw_station['latitude'],
            'longitude': raw_station['longitude'],
            'address': address,
            'description': raw_station['stationName'],
            'capacity': raw_station['totalDocks'],
            'available_bicycles': raw_station['availableBikes'],
            'available_docks': raw_station['availableDocks'],
            'is_active': raw_station['statusValue'] == 'In Service'

        }
        return station_id, station

    def parse_address(self, raw_station):
        result = ''
        if raw_station['stAddress1']:
            result += raw_station['stAddress1']
        if raw_station['stAddress2']:
            if result: result += ', '
            result += raw_station['stAddress2']
        return result