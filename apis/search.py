# Python modules
import os
import cgi
import Cookie

# Our own modules
from modules.location_searcher import *

# Google App Engine modules
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class SearchPage(webapp.RequestHandler):

    path = os.path.join(os.path.dirname(__file__), 'search.html')

    def get(self):
        isCookieSet = False
        currentLocation = ""
    
        cookie = Cookie.SimpleCookie()
        cookieString = os.environ.get('HTTP_COOKIE')
        
        if cookieString != None:
            isCookieSet = True

        template_values = {
            'isCookieSet': isCookieSet,
            'currentLocation': currentLocation
        }
        
        self.response.out.write(template.render(self.path, template_values))


application = webapp.WSGIApplication([('/apis/search.html', SearchPage)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
