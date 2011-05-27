import os
import cgi
import time
import Cookie
import string

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
        isQuakeSet = False
        isFBSet = False
        currentLocation = ""
    
        cookie = Cookie.SimpleCookie()
        cookieString = os.environ.get('HTTP_COOKIE')
        
        fbreturn = ""
        access_token = ""
        expires = ""
        infoString = ""
        coords = ""
        region = ""
        
        if cookieString != None:
            cookie.load(cookieString)
            if "fbreturn" in cookie:
                fbreturn = cookie["fbreturn"].value
                if fbreturn != "":
                    isFBSet = True
                    access_token = fbreturn.split('&')[0].replace("access_token=","")
                    expires = fbreturn.split('&')[1].replace("expires=","")
                    
                    friendsInfo = getAllFriendsInfo(access_token)
                    
                    for singleFriend in friendsInfo:
                        infoString += string.join(singleFriend[1:], ';') + '|'

            if ('geocode' in cookie) and 'region' in cookie:
                coords = cookie['geocode'].value
                coords = coords.replace(" ", "")
                region = cookie['region'].value
                isQuakeSet = True


        template_values = {
            'isQuakeSet': isQuakeSet,
            'isFBSet': isFBSet,
            'access_token': access_token,
            'expires': expires,
            'infoString': infoString,
            'region': region,
            'coords': coords
        }
        
        self.response.out.write(template.render(self.path, template_values))

application = webapp.WSGIApplication([('/apis/friends.html', FriendsPage)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
