__author__ = 'zats'


from wsgi.bicycle import SERVICES, scrape_for_service


print("Hello from the scraper")
for service in SERVICES.keys():
    print("Scraping for '%s'" % service)
    try:
        scrape_for_service(service)
    except Exception as e:
        print("Failed to scrape for '%s'" % service)


