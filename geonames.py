import settings
import httplib
import simplejson
import sys
from urllib import urlencode

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
        c = httplib.HTTPConnection(self.server)
        return c
    
    
                
class GeoNameException(Exception):
    """
    Error initializing GeoNames accessor.
    """
    def __init__(self, value):
        self.message = value
    def __str__(self):
        return repr(self.message)