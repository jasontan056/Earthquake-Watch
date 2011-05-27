import urllib2

from django.utils import simplejson as json

# get friends' ids using FB API 
# parse out friends' FB IDs
# rawIds is in the following form
# [12312,12343,34543,...]
# src: http://developers.facebook.com/docs/reference/rest/friends.get/
# example call https://api.facebook.com/method/friends.get?access_token=204588852914237|2.AQClZGYorXonFpM0.3600.1306267200.0-1608994936|vOInngu8dxJuZ6Q0adfSgankI_A&format=json
# param[IN] the access token
# returns a list of FB IDs
def parseFriendsIds(accessToken):
    # download the result returned by FB API
    url = "https://api.facebook.com/method/friends.get?access_token=" + accessToken + "&format=json"
    webpage = urllib2.urlopen(url)
    rawIds = webpage.read()
    
    # parse out the ids
    rawIds = rawIds[1:-1]
    idList = rawIds.split(",")
    
    return idList

# get friend information
# parse out friend's id, name, current addr, contact ino
# param[IN] access token
# param[IN] the friend id
# returns a tuples that
# contains friend's id, name, current addr
# in the given order
def getFriendInfo(accessToken, friendId):
    # download the result returned by FB API
    url = " https://graph.facebook.com/" + friendId + "?access_token=" + accessToken
    webpage = urllib2.urlopen(url)
    rawInfo = webpage.read()
    
    id = ""
    name = ""
    addr = ""
    addrId = ""
    lat = ""
    lng = ""
    friendLoc = ""
    link = ""
    
    # parse out info
    if rawInfo != "":
        obj = json.loads(rawInfo)
        
        if 'id' in obj:
            id = obj['id']
        
        if 'name' in obj:
            name = obj['name']
            
        if "link" in obj:
            link = obj["link"]
            
        if 'location' in obj:
            if 'name' in obj['location']:
                addr = obj['location']['name']
            if 'id' in obj['location']:
                addrId = obj['location']['id']
                url = "https://graph.facebook.com/" + addrId + "/?access_token=" + accessToken
                webpage = urllib2.urlopen(url)
                rawInfo = webpage.read()
                
                obj = json.loads(rawInfo)
                if "location" in obj:
                    lat = str(obj["location"]["latitude"])
                    lng = str(obj["location"]["longitude"])
                    friendLoc = lat + "," + lng
                    
    return (id, name, addr, friendLoc, link)
    
# returns a list of tuples
# each tuple contains the (id, name, addr) of the friend
# param[IN] accessToken to access a user's FB account
# returns a list of tuples that contains friend's info
def getAllFriendsInfo(accessToken):
    friendsInfoList = []
    idList = parseFriendsIds(accessToken)
    
    for id in idList:
        singleFriendInfo = getFriendInfo(accessToken, id)
        friendsInfoList.append(singleFriendInfo)
        
    return friendsInfoList