import settings
import httplib
import simplejson
import sys

from urllib import urlencode
from xml.etree import ElementTree

class GeoNames():
    """
    Accessor class for the online GeoNames geographical database. 
    """
    def __init__(self, server=settings.DEFAULT_GEONAMES_SERVER):
        """
        Create a GeoNames object.
        
            server - address of the server which provides REST webservice interface.
        """
        self.server = server
    
    def _api_call(self, method, resource, **kwargs):
        """
        Makes a generic API call to geonames webservice.
        """
        uri = "/%s?%s" %(resource, urlencode(kwargs))
        c = self.get_connection()
        c.request(method, uri)
        response = c.getresponse()
        if not 200 == response.status:
            raise GeoNameException("Expected a 200 reponse but got %s." %(response.status))
        return response.read()
                
    def get_connection(self):
        """
        Return a connection object to the webservice.
        """
        c = httplib.HTTPConnection(self.server)
        return c
        
    def search(self, name, country):
        """
        Perform a search for a country's information.
        """
        # we only want exact matches, and we only want one possible match.
        xml = self._api_call('GET', 'search', name_equals=name, country=country, maxRows=1)
        root_element = ElementTree.XML(xml)
        results = root_element.find('totalResultsCount').text
        if not results:
            raise GeoNameResultException("No results returned for query.")
        return GeoResult(
            name = root_element.find('geoname/name').text,
            country_name = root_element.find('geoname/countryName').text,
            country_code = root_element.find('geoname/countryCode').text,
            latitude = root_element.find('geoname/lat').text,
            longitude = root_element.find('geoname/lng').text,   
        )
            
    
class GeoResult(object):
    """
    Result object stores data returned from GeoNames api accessor object.
    """
    def __init__(self, name=None, country_name=None, country_code=None, latitude=None, longitude=None):
        self.name = name
        self.country_name = country_name
        self.country_code = country_code
        self.latitude = latitude
        self.longitude = longitude
        
    def is_complete(self):
        complete = True
        for key, val in self.__dict__.items():
            if not val:
                complete = False
                break
        return complete
                
                
class GeoNameException(Exception):
    """
    Error initializing GeoNames accessor.
    """
    def __init__(self, value):
        self.message = value
    def __str__(self):
        return repr(self.message)
        
class GeoNameResultException(GeoNameException):
    """
    Error getting results from GeoName webservice.
    """
    pass