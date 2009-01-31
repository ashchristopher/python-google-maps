import settings



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