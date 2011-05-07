# Python modules
import os
import cgi

# Our own modules
from modules.quake_parser import *

# Google App Engine Modules
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class GoogleMapPage(webapp.RequestHandler):

    path = os.path.join(os.path.dirname(__file__), 'googlemap.html')
    # This will be changed to user's computer's coords.
    defaultCoords = "34,-118" 
    def get(self):
        coordsToGo = self.request.get('coords')
        if coordsToGo == "":
            coordsToGo = self.defaultCoords

        template_values = {
            'coordsToGo': coordsToGo,
            'quake_coords': quake_parser()
        }
        
        self.response.out.write(template.render(self.path, template_values))

application = webapp.WSGIApplication([('/apis/googlemap.html', GoogleMapPage)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
