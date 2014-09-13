__author__ = 'zats'


import re
from bs4 import BeautifulSoup
from wsgi.custom_exceptions import ParsingErrorException
from wsgi.scrapers.base_scraper import BaseScraper


class TelofunScraper(BaseScraper):
    def service_name(self):
        return 'telofun'

    def service_url(self):
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

        regex = "setMarker\(([\d\.\-]+),([\d\.\-]+),([\d]+),'(.*?)','(.*?)','(\d*?)', '(\d*?)'"
        raw_markers = re.findall(regex, script)
        markers = {}
        for raw_marker in raw_markers:
            marker = self.parse_marker(raw_marker)
            station_id = marker['station_id']
            markers[station_id] = marker
        return markers

    def parse_marker(self, marker_object):
        capacity = int(marker_object[5])
        available_poles = int(marker_object[6])
        available_bicycles = capacity - available_poles
        result = {
            'latitude': float(marker_object[0]),
            'longitude': float(marker_object[1]),
            'station_id': marker_object[2],
            'address': marker_object[3],
            'description': marker_object[4],
            'capacity': capacity,
            'available_bicycles': available_bicycles,
            'available_poles': available_poles,
            'is_active': capacity > 0
        }
        return result

