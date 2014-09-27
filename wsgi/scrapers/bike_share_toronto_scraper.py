
__author__ = 'zats'


from wsgi.Mapping import CoordinateRegion
from wsgi.scrapers.base_scraper import ServiceRegion
from wsgi.scrapers.daniel_gohlike_scraper import DanielGohlkeScrapper


class BikeShareTorontoScraper(DanielGohlkeScrapper):

    @classmethod
    def service_regions(cls):
        return [ServiceRegion('Toronto', CoordinateRegion(43.63259596413715, -79.42168431854248, 43.674886486162606, -79.35516553497314))]

    @classmethod
    def name(cls):
        return 'Bike Share'

    @classmethod
    def timezone_name(cls):
        return 'America/Toronto'

    @classmethod
    def service_id(cls):
        return 'bikesharetoronto'

    @classmethod
    def website_url(cls):
        return 'http://www.bikesharetoronto.com'

    def service_url(self):
        return 'http://www.bikesharetoronto.com/stations/json'

    def parse_address(self, raw_station):
        return raw_station['stationName']
