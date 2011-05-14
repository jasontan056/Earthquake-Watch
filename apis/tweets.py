# Python modules
import os
import cgi
import time
import Cookie

# Our own modules
from modules.tweets_searcher import *

# Google App Engine Modules
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class TweetsPage(webapp.RequestHandler):

    path = os.path.join(os.path.dirname(__file__), 'tweets.html')
    
    def get(self):
        cookie = Cookie.SimpleCookie()
        cookieString = os.environ.get('HTTP_COOKIE')
        
        tweets = []
        isResultEmpty = False
        isCookieSet = False
        
        region = ""
        
        if cookieString != None:
            isCookieSet = True
            cookie.load(cookieString)
            
            coords = cookie['geocode'].value
            coords = coords.replace(" ", "")
            
            region = cookie['region'].value
            
            if coords != "":
                for i in range(0,10):
                    rawTweets = getTweets(coords)
                    tweets = parseTweets(rawTweets)
                    if tweets != []:
                        break
                    time.sleep(1)
                
            if tweets == []:
                isResultEmpty = True
                
        template_values = {
            'tweets': tweets,
            'isResultEmpty': isResultEmpty,
            'isCookieSet': isCookieSet,
            'region': region
        }
        
        self.response.out.write(template.render(self.path, template_values))

application = webapp.WSGIApplication([('/apis/tweets.html', TweetsPage)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
