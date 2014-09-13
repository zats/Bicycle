__author__ = 'zats'


import inspect
from wsgi.scrapers.base_scraper import BaseScraper
from wsgi.bicycle import *

with app.app_context():
    print("Hello from the scraper")
    for scraperClass in BaseScraper.__subclasses__():
        try:
            print("Scraping for '%s'" % scraperClass)
            scraper = scraperClass()
            service_name = scraper.service_name()
            print("Processing service %s" % service_name)
            scrape_for_service(service_name, False)
        except Exception as e:
            print("Failed to scrape '%s'" % e)


