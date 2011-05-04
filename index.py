# Python modules
import os
import cgi

# Our own modules
from modules.inputhandler import *
from modules.locationsearcher import *
from modules.jsonparser import *
from modules.quake_parser import *

# Google App Engine Modules
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class MainPage(webapp.RequestHandler):
    path = os.path.join(os.path.dirname(__file__), 'index.html')

    def get(self):
        zoom = 10
        # The location the user see when s/he opens up the browser.
        initialLocation = "34.07, -118.44"
        # The city name the user see when s/he opens up the browser.
        currentCity = "Los Angeles, CA, USA"
        # The parsed location is empty at first.
        isParsedLocationsEmpty = True
        # init is true when the user opens up the browser.
        init = True
        
        template_values = {
            'coords': initialLocation,
            'zoom': zoom,
            'isParsedLocationsEmpty': isParsedLocationsEmpty,
            'init': init,
            'currentCity': currentCity,
	    'quake_coords': quake_parser()
        }
        self.response.out.write(template.render(self.path, template_values))

    def post(self):
        # inputLocation is the user's location input.
        inputLocation = self.request.get('search')
        # cityToWatch is the user's choice when the location is ambiguous
        cityToWatch = self.request.get('choice')
        # If the user enters something, init becomes false.
        init = False
        zoom = 10
        
        # If the user enters nothing the current city keeps the same.
        currentCity = ""
        if inputLocation == "":
            init = True
            currentCity = "Los Angeles, CA, USA"
        
        # Sanitize the inputLocation for Google Map search.
        sanitizedlocation = sanitize(inputLocation)
        # Get the data google returns.
        googleResult = getGoogleResult(sanitizedlocation)
        # A list of parsed locations.
        parsedLocations = parseGoogleLocation(googleResult)
        
        isParsedLocationsEmpty = False
        # If parsedLocations is empty set it to false.
        if len(parsedLocations) == 0:
            isParsedLocationsEmpty = True
        
        # cityToWatch is in (lat, lng|city name) format.
        coords = ""
        if cityToWatch != "":
            coords = cityToWatch.split('|')[0]
            currentCity = cityToWatch.split('|')[1]
        else:
            coords = "34.07, -118.44"

        template_values = {
            'coords': coords,
            'zoom': zoom,
            'parsedLocations': parsedLocations,
            'isParsedLocationsEmpty' : isParsedLocationsEmpty,
            'init': init,
            'currentCity': currentCity,
	    'quake_coords': quake_parser()
        }
        self.response.out.write(template.render(self.path, template_values))

application = webapp.WSGIApplication([('/', MainPage)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
