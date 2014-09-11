__author__ = 'zats'


import urllib


DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 5.1; rv:31.0) ' \
                     'Gecko/20100101 Firefox/31.0'


class BaseScraper(object):
    @abstractmethod
    def service_url(self):
        return None

    @abstractmethod
    def scrape(self, url):
        pass

    @classmethod
    def open_url(cls, url, referer=None, user_agent=None):
        """ read url
        """

        request = urllib.request.Request(url)
        user_agent = user_agent if user_agent else DEFAULT_USER_AGENT
        request.add_header('User-Agent', user_agent)
        if referer:
            request.add_header('Referer', referer)
        response = urllib.request.urlopen(request)
        page = response.read()
        return page