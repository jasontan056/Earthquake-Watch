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
        # remove the trailing new line character
        line = line.replace('\n',"")

        # break up the information
    	splitLine = line.split(',')
        eqid = splitLine[1]

        # get the earthquake time, remove quotes
        time = splitLine[3]+", "+splitLine[4]+", " + splitLine[5]
        time = time.replace("\"","")

        # get coords of the earthquake
        coords = splitLine[6]+", "+splitLine[7]

        # get magnitude
        magnitude = splitLine[8]

        # get depth
        depth = splitLine[9]

        # get location, remove quotes, remove last character
        location = ",".join(splitLine[11:])
        location = location.replace("\"","")
        location = location.replace("\'","\\'")
        location = location[0:-1]

        # pack all the information up in a tuple
        info = (eqid, time, coords, magnitude, depth, location)

        # append the tuple to the list
        quakeInfo.append(info)

    return quakeInfo
