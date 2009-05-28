import PyRSS2Gen
import types

def _seq_to_string(l):
    """
        Take an argument which may be a string or may be sequence.
        if it's a string, return it unchanged; otherwise, return a string which has 
        one space between each element as typical for GeoRSS formatting.
        
        Nothing is done to ensure that the string is formatted correctly, 
        nor that the values of the sequence are correctly formatted. You're on
        your own for that.
    """
    if type(l) in types.StringTypes:
        return l
    return " ".join(l)
    
class GeoRSSFeed(PyRSS2Gen.RSS2):
    """Add the 'georss' namespace to the generated feed."""
    def __init__(self,*args,**kwargs):
        PyRSS2Gen.RSS2.__init__(self, *args, **kwargs)
        self.rss_attrs['xmlns:georss'] = 'http://www.georss.org/georss'

class GeoRSSItem(PyRSS2Gen.RSSItem):
    """
        Add the following properties to an RSSItem, with support for rendering them 
        in the "simple" representation.
            * point (sequence)
            * line (sequence)
            * polygon (sequence)
            * box (sequence)
            * featuretypetag
            * relationshiptag
            * featurename
            * elev
            * floor
            * radius
            
        Each of these may be a string.  The types labeled "sequence" may also be a 
        sequence, in which case they will be joined with whitespace separators according
        to the GeoRSS standards.
        
        See http://www.georss.org/simple for more information.
    """
    properties = [
        'point',
        'line',
        'polygon',
        'box',
        'featuretypetag',
        'relationshiptag',
        'featurename',
        'elev',
        'floor',
        'radius',
    ]

    point = None
    line = None
    polygon = None
    box = None
    featuretypetag = None
    relationshiptag = None
    featurename = None
    elev = None
    floor = None
    radius = None

    def publish_extensions(self, handler):
        for p in GeoRSSItem.properties:
            value = getattr(self,p)
            if value is not None:
                PyRSS2Gen._element(handler,"georss:%s" % p, _seq_to_string(value))    

    def __init__(self,**kwargs):
        geokwargs = {}
        for p in GeoRSSItem.properties:
            if kwargs.has_key(p):
                geokwargs[p] = kwargs.pop(p)
        PyRSS2Gen.RSSItem.__init__(self, **kwargs)
        for key in geokwargs:
            setattr(self,key,geokwargs[key])
