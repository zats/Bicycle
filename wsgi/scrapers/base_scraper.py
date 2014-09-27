
__author__ = 'zats'

from abc import ABCMeta, abstractmethod
import urllib
import urllib.request
from wsgi.Mapping import CoordinateRegion


DEFAULT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) ' \
                     'AppleWebKit/600.1.15 (KHTML, like Gecko) Version/8.0 Safari/600.1.15'


class ServiceRegion(object):

    def __init__(self, city: str, region: CoordinateRegion):
        self.city = city
        self.region = region


class BaseScraper(object, metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def service_regions(cls):
        pass

    @classmethod
    @abstractmethod
    def name(cls):
        pass

    @classmethod
    @abstractmethod
    def service_id(cls):
        pass

    @classmethod
    @abstractmethod
    def website_url(cls):
        pass

    @classmethod
    @abstractmethod
    def timezone_name(cls):
        pass

    @abstractmethod
    def service_url(self):
        pass

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
        encoding = response.headers.get_content_charset() or 'utf-8'
        return response.read().decode(encoding)