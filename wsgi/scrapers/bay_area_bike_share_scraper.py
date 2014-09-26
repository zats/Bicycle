__author__ = 'zats'


from wsgi.scrapers.daniel_gohlike_scraper import DanielGohlkeScrapper


class BayAreaBikeShareScraper(DanielGohlkeScrapper):
    def service_name(self):
        return 'bayareabikeshare'

    def service_url(self):
        return 'http://www.bayareabikeshare.com/stations/json'

    def parse_address(self, raw_station):
        return raw_station['location']
