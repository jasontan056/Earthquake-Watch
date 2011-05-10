# Python modules
import os
import cgi

# Our own modules
from modules.inputhandler import *
from modules.locationsearcher import *
from modules.jsonparser import *

# Google App Engine modules
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class SearchPage(webapp.RequestHandler):

    path = os.path.join(os.path.dirname(__file__), 'search.html')
    currentLocation = ""
    userLocation = "will be modified later"

    def get(self):
        # init is true whenever the page is loaded.
        init = True

        # currentLocation is the city displayed below the input box.
        if self.currentLocation == "":
            self.currentLocation = self.userLocation

        template_values = {
            'init': init,
            'currentLocation': self.currentLocation
        }
        
        self.response.out.write(template.render(self.path, template_values))

    def post(self):
        # After the user enters something, init becomes false
        init = False

        # currentLocation is the city displayed below the input box.
        self.currentLocation = self.request.get('preLocationPost')
        if self.currentLocation == "":
            self.currentLocation = self.userLocation

        # Get user's input.
        inputLocation = self.request.get('search')
        cityToWatch = self.request.get('choice')

        # currentLocation is the city displayed below the input box.
        if cityToWatch !="":
            self.currentLocation = cityToWatch
            init = True
            
        # Get location results from Google Geocoding.
        parsedLocations = []
        if inputLocation != "":
            sanitizedlocation = sanitize(inputLocation)
            googleResult = getGoogleResult(sanitizedlocation)
            parsedLocations = parseGoogleLocation(googleResult)

        # Check if the parsedLocations is empty
        isParsedLocationsEmpty = False
        if len(parsedLocations) == 0:
            isParsedLocationsEmpty = True

        template_values = {
            'parsedLocations': parsedLocations,
            'init': init,
            'isParsedLocationsEmpty': isParsedLocationsEmpty,
            'inputLocation': inputLocation,
            'currentLocation': self.currentLocation,
            'previousLocation': self.currentLocation,
        }

        self.response.out.write(template.render(self.path, template_values))


application = webapp.WSGIApplication([('/apis/search.html', SearchPage)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
