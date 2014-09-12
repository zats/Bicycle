__author__ = 'zats'


from wsgi.bicycle import SERVICES


print("Hello from the scraper")
for service in SERVICES.keys():
    print("service %s" % service)
