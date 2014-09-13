__author__ = 'zats'


import inspect
from wsgi.scrapers.base_scraper import BaseScraper
from wsgi.bicycle import *

with app.app_context():
    for service_id, service_dict in SERVICES.items():
        print("Hello from the scraper %s" % service_id)
        try:
            scrape_for_service(service_id, False)
        except Exception as e:
            print("Failed to scrape '%s'" % e)
