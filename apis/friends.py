import os
import cgi
import time
import Cookie

# Our own modules
from modules.friends_searcher import *

# Google App Engine Modules
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class FriendsPage(webapp.RequestHandler):

    path = os.path.join(os.path.dirname(__file__), 'friends.html')
    
    def get(self):
        isCookieSet = False
        currentLocation = ""
    
        cookie = Cookie.SimpleCookie()
        cookieString = os.environ.get('HTTP_COOKIE')
        
        fbreturn = ""
        access_token = ""
        expires = ""
        if cookieString != None:
            cookie.load(cookieString)
            
            if "fbreturn" in cookie:
                fbreturn = cookie["fbreturn"].value
                if fbreturn != "":
                    isCookieSet = True
                    access_token = fbreturn.split('&')[0].replace("access_token=","")
                    expires = fbreturn.split('&')[1].replace("expires=","")

        template_values = {
            'isCookieSet': isCookieSet,
            'access_token': access_token,
            'expires': expires
        }
        
        self.response.out.write(template.render(self.path, template_values))

application = webapp.WSGIApplication([('/apis/friends.html', FriendsPage)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
