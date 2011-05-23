# Python modules
import os
import cgi
import time
import Cookie

# Our own modules
from modules.photo_searcher import *

# Google App Engine modules
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class PhotosPage(webapp.RequestHandler):

    path = os.path.join(os.path.dirname(__file__), 'photos.html')
    
    def get(self):
        # get cookie
        cookie = Cookie.SimpleCookie()
        cookieString = os.environ.get('HTTP_COOKIE')
        
        photolist = []
        region = ""

        isResultEmpty = False
        isCookieSet = False
        
        # check if cookie exists
        if cookieString != None:
            cookie.load(cookieString)
            
            # check if the value is set
            if 'region' in cookie:
                region = cookie['region'].value
                isCookieSet = True
            
            # parse out the information of the json file
            if region != "":
                jsonFile = searchPhotos(region)
                photolist = parsePhotos(jsonFile)
                
                #group photolist into a list of a list, each list contains three photos
                tuplelist = []
                sublist = []
                for i in range(len(photolist)):
                    if (i + 1) % 4 == 0:
                        sublist.append(photolist[i])
                        tuplelist.append(sublist)
                        sublist = []
                    else:
                        sublist.append(photolist[i])
                tuplelist.append(sublist)
                
        
            # check if the result is empty
            if photolist == []:
                isResultEmpty = True
        
        
        template_values = {
            'tuplelist': tuplelist,
            'isResultEmpty': isResultEmpty,
            'isCookieSet': isCookieSet,
            'region' : region
        }
        
        self.response.out.write(template.render(self.path, template_values))

application = webapp.WSGIApplication([('/apis/photos.html', PhotosPage)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
