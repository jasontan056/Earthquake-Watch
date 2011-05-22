# Python modules
import os
import cgi
import time
import Cookie
import urllib
import flickrapi

# Our own modules
from modules.photos_parser import *

# Google App Engine modules
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class PhotosPage(webapp.RequestHandler):

    path = os.path.join(os.path.dirname(__file__), 'photos.html')
    
    def get(self):
        cookie = Cookie.SimpleCookie()
        cookieString = os.environ.get('HTTP_COOKIE')
        
        photolist = []
        region = ""
        coords = ""
        isResultEmpty = False
        isCookieSet = False
        
        if cookieString != None:
            cookie.load(cookieString)
            
            if ('geocode' in cookie) and 'region' in cookie:
                coords = cookie['geocode'].value
                coords = coords.replace(" ", "")
                region = cookie['region'].value
                isCookieSet = True
            
            if region != "":
                apikey = '1ce8a15c20b6fcc0a71d27dbeaa8cfac'
                flickr = flickrapi.FlickrAPI(apikey)
                tag='Earthquake, '+region
                # from http://www.flickr.com/services/api/flickr.photos.search.html
                # TODO: use min_upload_date? how do I get the today's date?
                # TODO: use lat or lon? probably not...
                rawphotolist = flickr.photos_search(api_key=apikey, tags=tag, tag_mode='all', format='json')
                photolist = parsePhotos(rawphotolist)
        
            if photolist == []:
                isResultEmpty = True
        
        
        template_values = {
            'photolist': photolist,
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
