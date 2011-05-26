# Python modules
import os
import cgi
import urllib2
import Cookie

# Google App Engine Modules
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class MainPage(webapp.RequestHandler):
    path = os.path.join(os.path.dirname(__file__), 'index.html')
        
    def get(self):
        appId = "204588852914237"
        appURL = "http://earthquake-watch.appspot.com/"
        appSecret = "375ec6dfa7c26eeeb43accf929c15501"
        code = self.request.get('code')
        url = "https://graph.facebook.com/oauth/access_token?client_id=" + appId + "&redirect_uri=" + appURL + "&client_secret="+appSecret+"&code="+code
        
        template_values = {
        }
        
        access_token = ""
        try:
            webpage = urllib2.urlopen(url)
            access_token = webpage.read()
        except:
            self.response.out.write(template.render(self.path, template_values))
        else:
            template_values = {
                'access_token': access_token
            }
            self.response.out.write(template.render(self.path, template_values))


application = webapp.WSGIApplication([('/', MainPage)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
