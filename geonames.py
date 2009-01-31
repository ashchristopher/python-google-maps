import settings
import httplib
import simplejson
import sys

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
        # protect against infinite redirect loop.
        self._connect()
                
    def _connect(self):
        # protect against infinite redirect loop.
        redirects = []
        server_found = False
        
        while not server_found:
            self.c = httplib.HTTPConnection(self.server)
            # check server redirect.
            self.c.request('GET', '/search')    # REST interface should have index.
            response = self.c.getresponse()
            if response.status == 200:
                server_found = True
            elif response.status == 301:
                redirects.append(self.server)
                # get server to redirect to.
                # TODO: lets use a regular expression here - need the server name only.
                self.server = response.getheader('location').replace('http://', '').replace('/', '')
                if self.server in redirects:
                    print redirects
                    raise GeoNameInitException("Infinte re-direct loop detected.")
                self.c = httplib.HTTPConnection(self.server)
                sys.stderr.writelines("R301: Using new server '%s'" %(self.server))
    
                
class GeoNameInitException(Exception):
    """
    Error initializing GeoNames accessor.
    """
    def __init__(self, value):
        self.message = value
    def __str__(self):
        return repr(self.message)