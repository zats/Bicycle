__author__ = 'zats'


import inspect
import newrelic.agent
from wsgi.scrapers.base_scraper import BaseScraper
from wsgi.bicycle import *

with app.app_context():
    newrelic_app = newrelic.agent.application()
    with newrelic.agent.BackgroundTask(newrelic_app, name='scraper', group='Task'):
        for service_id, service_dict in SERVICES.items():
            print("Hello from the scraper %s" % service_id)
            try:
                scrape_for_service(service_id, False)
            except Exception as e:
                print("Failed to scrape '%s'" % e)
