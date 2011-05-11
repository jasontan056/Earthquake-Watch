# Python modules
import os
import cgi

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
        coords = self.request.get('coords').replace(" ", "")
        
        tweets = []
        if coords != "":
            rawTweets = getTweets(coords)
            tweets = parseTweets(rawTweets)
            
        isResultEmpty = True
        if tweets != []:
            isResultEmpty = False

        template_values = {
            'tweets': tweets,
            'isResultEmpty': isResultEmpty
        }
        
        self.response.out.write(template.render(self.path, template_values))

application = webapp.WSGIApplication([('/apis/tweets.html', TweetsPage)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
