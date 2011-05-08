import urllib2
import string

# Returns the earthquake information in a list of tuple.
# The tuples are in the form: (eqid, time, coords, magnitude, depth, location)
def quake_parser():
    response = urllib2.urlopen('http://earthquake.usgs.gov/earthquakes/catalogs/eqs7day-M5.txt')
    feed = response.read().split('\n')
    #remove the first and the last lines from the feed
    del feed[0]
    del feed[len(feed)-1]
    #build a list of earthquake coordinates
    quakeInfo = []
    for line in feed:
    	splitLine = line.split(',')
        eqid = splitLine[1]
        time = splitLine[3]+", "+splitLine[4]+", " + splitLine[5]
        time = time.replace("\"","")
        coords = splitLine[6]+", "+splitLine[7]
        magnitude = splitLine[8]
        depth = splitLine[9]
        location = "".join(splitLine[11:])
        location = location.replace("\"","")
        location = location.replace("\'","")
        info = (eqid, time, coords, magnitude, depth, location)
        quakeInfo.append(info)
    return quakeInfo
