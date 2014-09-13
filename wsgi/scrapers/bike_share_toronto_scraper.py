__author__ = 'zats'


from wsgi.scrapers.daniel_gohlike_scraper import DanielGohlkeScrapper


class BikeShareTorontoScraper(DanielGohlkeScrapper):
    def service_name(self):
        return 'bikesharetoronto'

    def service_url(self):
        return 'http://www.bikesharetoronto.com/stations/json'
