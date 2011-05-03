import urllib

# This function returns the search of location in json format.
def getGoogleResult(location):
    url = "http://maps.googleapis.com/maps/api/geocode/json?address="+location+"&sensor=true"
    webpage = urllib.urlopen(url)
    return webpage.read()