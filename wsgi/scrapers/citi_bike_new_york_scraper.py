
__author__ = 'zats'


from wsgi.Mapping import CoordinateRegion
from wsgi.scrapers.base_scraper import ServiceRegion
from wsgi.scrapers.daniel_gohlike_scraper import DanielGohlkeScrapper


class CitiBikeNewYorkScraper(DanielGohlkeScrapper):

    @classmethod
    def google_maps_region(cls):
        return [40.720952, -73.9822521, 13]

    @classmethod
    def service_regions(cls):
        return [ServiceRegion('New York', CoordinateRegion(40.673863788197906, -74.02186112976074, 40.769227266751166, -73.93534379577636))]

    @classmethod
    def name(cls):
        return 'Citi Bike'

    @classmethod
    def timezone_name(cls):
        return 'America/New_York'

    @classmethod
    def service_id(cls):
        return 'citibikenyc'

    @classmethod
    def website_url(cls):
        return 'https://www.citibikenyc.com'

    def service_url(self):
        return 'https://www.citibikenyc.com/stations/json'
