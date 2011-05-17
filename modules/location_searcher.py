import urllib2
from django.utils import simplejson as json

# This function returns the search of location in json format.
def getGoogleResult(location):
    url = "http://maps.googleapis.com/maps/api/geocode/json?address="+location+"&sensor=true"
    webpage = urllib2.urlopen(url)
    return webpage.read()

# This function returns a list of tuples.
# First element of the tuple is the formated address of the city.
# Second element of the tuple is the coordinate of the city.
def parseGoogleLocation(jsondata):
    obj = json.loads(jsondata)
    status = obj["status"]
    
    parsed = []
    
    if status == "OK":
        results = obj["results"]
        for places in results:
            formatted = places["formatted_address"]
            location = places["geometry"]["location"]
            lat = location["lat"]
            lng = location["lng"]
            coords = str(lat)+", "+str(lng)
            single = (formatted, coords)
            parsed.append(single)

    return parsed