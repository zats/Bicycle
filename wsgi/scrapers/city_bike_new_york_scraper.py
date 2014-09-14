__author__ = 'zats'


from wsgi.scrapers.daniel_gohlike_scraper import DanielGohlkeScrapper


class CityBikeNewYorkScraper(DanielGohlkeScrapper):
    def service_name(self):
        return 'citibikenyc'

    def service_url(self):
        return 'https://www.citibikenyc.com/stations/json'
