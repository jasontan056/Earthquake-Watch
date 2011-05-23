import urllib2

from django.utils import simplejson as json

# returns the flickr api result in json format
def searchPhotos(region):
    # remove the "," between locations
    region = region.replace(",","")
    # form a list of fields of the locations
    regionFields = region.split(" ")
    
    # form the region in a general version
    # eg "off the east coast of Honshu, Japan" -> "Honshu Japan"
    shortName = ""
    for field in regionFields:
        if field[0].isupper():
            shortName += ','+field
    
    # search for the photos
    # the keyword will be "Earthquake,Honshu,Japan"
    apikey = '1ce8a15c20b6fcc0a71d27dbeaa8cfac'
    tag="Earthquake" + shortName
    url = "http://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=" + apikey + "&tags=" + tag + "&format=json&tag_mode=all"
    webpage = urllib2.urlopen(url)
    jsonFile = webpage.read()
    
    # parse out the json file
    jsonFile = jsonFile[14:-1]
    
    return jsonFile

# parse out the information in the json file
# returns a list of tuples
def parsePhotos(rawPhotos):
    parsed = []
    
    if rawPhotos != "":
        obj = json.loads(rawPhotos)
        stat = obj["stat"]
        
        if stat == "ok":
            photos = obj["photos"]["photo"]
            
            for photo in photos:
                id = photo["id"]
                secret = photo["secret"]
                server = photo["server"]
                farm = photo["farm"]                
                single = (farm, server, id, secret)
                parsed.append(single)
    
    return parsed
        
