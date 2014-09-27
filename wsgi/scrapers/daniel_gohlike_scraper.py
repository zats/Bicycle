__author__ = 'zats'


import json
from abc import ABCMeta
from wsgi.scrapers.base_scraper import BaseScraper


class DanielGohlkeScrapper(BaseScraper, metaclass=ABCMeta):

    def scrape(self, url):
        json_data = self.open_url(url)
        data = json.loads(json_data)

        result = {}
        for raw_station in data['stationBeanList']:
            station_id, marker = self.parse_stations(raw_station)
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
            'is_active': self.is_station_active(raw_station)
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

    def is_station_active(self, raw_station):
        return raw_station['statusValue'] == 'In Service' and raw_station['testStation'] is False
