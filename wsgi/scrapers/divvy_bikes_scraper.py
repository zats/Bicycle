__author__ = 'zats'


from wsgi.scrapers.daniel_gohlike_scraper import DanielGohlkeScrapper


class DivvyBikesScraper(DanielGohlkeScrapper):
    def service_name(self):
        return 'divvybikes'

    def service_url(self):
        return 'https://www.divvybikes.com/stations/json'
