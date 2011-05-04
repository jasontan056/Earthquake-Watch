import urllib2
import string

def quake_parser():
    response = urllib2.urlopen('http://earthquake.usgs.gov/earthquakes/catalogs/eqs7day-M5.txt')
    feed = response.read().split('\n')
    #remove the first and the last lines from the feed
    del feed[0]
    del feed[len(feed)-1]
    #build a list of earthquake coordinates
    coordList = []
    for line in feed:
    	splitLine = line.split(',')
	coordList.append((splitLine[6], splitLine[7]))
    return coordList
