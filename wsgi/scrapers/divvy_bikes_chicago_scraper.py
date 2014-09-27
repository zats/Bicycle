__author__ = 'zats'


from wsgi.Mapping import CoordinateRegion
from wsgi.scrapers.base_scraper import ServiceRegion
from wsgi.scrapers.daniel_gohlike_scraper import DanielGohlkeScrapper


class DivvyBikesChicagoScraper(DanielGohlkeScrapper):

    @classmethod
    def service_regions(cls):
        return [ServiceRegion('Chicago', CoordinateRegion(41.788868493341305, -87.73643570518493, 41.99307281184169, -87.56340103721618))]

    @classmethod
    def timezone_name(cls):
        return 'America/Chicago'

    @classmethod
    def service_id(cls):
        return 'divvybikes'

    @classmethod
    def name(cls):
        return 'Divvy'

    @classmethod
    def website_url(cls):
        return 'https://www.divvybikes.com'

    def service_url(self):
        return 'https://www.divvybikes.com/stations/json'
