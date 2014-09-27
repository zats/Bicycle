__author__ = 'zats'


from wsgi.Mapping import CoordinateRegion
from wsgi.scrapers.base_scraper import ServiceRegion
from wsgi.scrapers.daniel_gohlike_scraper import DanielGohlkeScrapper


class BayAreaBikeShareScraper(DanielGohlkeScrapper):

    @classmethod
    def service_regions(cls):
        return [
            ServiceRegion('San Francisco', CoordinateRegion(37.77040895565292, -122.42414670562744, 37.810427677534456, -122.38088803863525)),
            ServiceRegion('Redwood City', CoordinateRegion(37.48097085917848, -122.2381301460266, 37.49457487526275, -122.22177939987182)),
            ServiceRegion('Palo Alto', CoordinateRegion(37.426397963287485, -122.16630058860778, 37.45406626635965, -122.1230419216156)),
            ServiceRegion('Mountain View', CoordinateRegion(37.38306903742909, -122.11875038719177, 37.41034429694875, -122.0644195613861)),
            ServiceRegion('San Jose', CoordinateRegion(37.328386371546515, -121.91644745445251, 37.35752357983567, -121.87318878746032))
        ]

    @classmethod
    def name(cls):
        return 'Bike Share'

    @classmethod
    def timezone_name(cls):
        return 'America/Los_Angeles'

    @classmethod
    def service_id(cls):
        return 'bayareabikeshare'

    @classmethod
    def website_url(cls):
        return 'http://www.bayareabikeshare.com'

    def service_url(self):
        return 'http://www.bayareabikeshare.com/stations/json'

    def parse_address(self, raw_station):
        return raw_station['location']
