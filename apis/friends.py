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
        allFriendsInfo = getAllFriendsInfo("204588852914237|2.AQClZGYorXonFpM0.3600.1306267200.0-1608994936|vOInngu8dxJuZ6Q0adfSgankI_A")
        template_values = {
            'allFriendsInfo': allFriendsInfo
        }
        
        self.response.out.write(template.render(self.path, template_values))

application = webapp.WSGIApplication([('/apis/friends.html', FriendsPage)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
