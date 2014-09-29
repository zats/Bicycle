__author__ = 'zats'


import re
from bs4 import BeautifulSoup
from wsgi.Mapping import *
from wsgi.custom_exceptions import ParsingErrorException
from wsgi.scrapers.base_scraper import BaseScraper, ServiceRegion


class TelofunScraper(BaseScraper):

    @classmethod
    def google_maps_region(cls):
        return [32.0765638, 34.7780845, 14]

    @classmethod
    def service_regions(cls):
        return [ServiceRegion('Tel Aviv', CoordinateRegion(32.05042486766724, 34.7494391860962, 32.125325127602984, 34.83595652008057))]

    @classmethod
    def name(cls):
        return 'Telofun'

    @classmethod
    def timezone_name(cls):
        return 'Asia/Jerusalem'

    @classmethod
    def service_id(cls):
        return 'telofun'

    @classmethod
    def website_url(cls):
        return 'https://www.tel-o-fun.co.il/en'

    @classmethod
    def service_url(cls):
        return 'https://www.tel-o-fun.co.il/en/TelOFunLocations.aspx'

    def scrape(self, url):
        content = self.open_url(url)
        soup = BeautifulSoup(content)
        scripts = soup.find_all("script")
        script = None
        for _ in scripts:
            _ = _.text
            if type(_) is not str or not _.startswith('function loadMarkers()'): continue
            script = _

        if script is None:
            raise ParsingErrorException()

        regex = "setMarker\(([\d\.\-]+),([\d\.\-]+),([\d]+),'(.*?)','(.*?)','([\d\-]*?)', '([\d\-]*?)'"
        raw_markers = re.findall(regex, script)
        markers = {}
        for raw_marker in raw_markers:
            (station_id, marker) = self.parse_marker(raw_marker)
            markers[station_id] = marker
        return markers

    @staticmethod
    def parse_marker(marker_object):
        station_id = marker_object[2]
        capacity = int(marker_object[5])
        if capacity < 0:
            capacity = 0
        available_docks = int(marker_object[6])
        if available_docks < 0:
            available_docks = 0
        available_bicycles = capacity - available_docks
        result = {
            'latitude': float(marker_object[1]),
            'longitude': float(marker_object[0]),
            'station_id': station_id,
            'address': marker_object[3],
            'description': marker_object[4],
            'capacity': capacity,
            'available_bicycles': available_bicycles,
            'available_docks': available_docks,
            'is_active': capacity > 0
        }
        return station_id, result

