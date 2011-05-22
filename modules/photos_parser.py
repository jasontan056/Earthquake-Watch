import urllib2
from django.utils import simplejson as json

def parsePhotos(rawPhotos):
    parsed = []
    
    if rawPhotos != "":
        obj = json.loads(rawPhotos)
        results = obj["results"]
        
        if results != []:
            for photo in results:
                photo_id = tweet["id"]
                secret = photo["secret"]
                server = photo["server"]
                farm = photo["farm"]                
                single = (photo_id, secret, server, farm)
                parsed.append(single)
    
    return parsed
        
