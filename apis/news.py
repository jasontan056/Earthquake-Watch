# Python modules
import os
import cgi

# Google App Engine modules
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class SearchPage(webapp.RequestHandler):

    path = os.path.join(os.path.dirname(__file__), 'news.html')

    def get(self):
    
        template_values = {
        }
        
        self.response.out.write(template.render(self.path, template_values))

application = webapp.WSGIApplication([('/apis/news.html', SearchPage)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
