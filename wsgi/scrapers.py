__author__ = 'zats'


import os
import newrelic.agent
config_file = os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'newrelic.ini')
newrelic.agent.initialize(config_file)
application = newrelic.agent.register_application(timeout=10.0)


from wsgi.bicycle import *
with app.app_context():
    for service_id, service_dict in scrapers.items():
        print("Hello from the scraper %s" % service_id)
        try:
            scrape_for_service(service_id, False)
        except Exception as e:
            print("Failed to scrape '%s'" % e)