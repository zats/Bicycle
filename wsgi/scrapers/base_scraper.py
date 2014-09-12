__author__ = 'zats'

from abc import ABCMeta, abstractmethod
import urllib


DEFAULT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) ' \
                     'AppleWebKit/600.1.15 (KHTML, like Gecko) Version/8.0 Safari/600.1.15'


class BaseScraper(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def service_name(self):
        return None


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