# Python modules
import os
import cgi
import Cookie

# Our own modules
from modules.quake_parser import *

# Google App Engine Modules
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class GoogleMapPage(webapp.RequestHandler):

    path = os.path.join(os.path.dirname(__file__), 'googlemap.html')
    
    def get(self):
        cookie = Cookie.SimpleCookie()
        cookieString = os.environ.get('HTTP_COOKIE')
        
        coords = "30,120"
        zoom = "3"
    
        if cookieString != None:
            cookie.load(cookieString)
            
            if 'geocode' in cookie:
                zoom = "7"
                coords = cookie['geocode'].value
                coords = coords.replace(" ", "")

        template_values = {
            'coordsToGo': coords,
            'zoom': zoom,
            'quake_coords': quake_parser()
        }
        
        self.response.out.write(template.render(self.path, template_values))

application = webapp.WSGIApplication([('/apis/googlemap.html', GoogleMapPage)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
