__author__ = 'zats'


from wsgi.scrapers.base_scraper import BaseScraper
from wsgi.bicycle import *

with app.app_context():
    print("Hello from the scraper")
    for scraperClass in BaseScraper.__subclasses__():
        print("Scraping for '%s'" % scraperClass)
        try:
            scraper = scraperClass()
            service_name = scraper.service_name()
            print("Processing service %s" % service_name)
            scrape_for_service(service_name)
        except Exception as e:
            print("Failed to scrape '%s'" % e)


