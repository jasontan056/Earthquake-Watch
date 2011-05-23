# python modules
import os
import cgi
import Cookie

# Google App Engine modules
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template


class VideosPage(webapp.RequestHandler):

	path = os.path.join(os.path.dirname(__file__), 'videos.html')

	def get(self):
		cookie = Cookie.SimpleCookie()
		cookieString = os.environ.get('HTTP_COOKIE')

		region = ''
		coords = ''
		isCookieSet = False

		if cookieString != None:
				cookie.load(cookieString)

				if ('geocode' in cookie) and ('region' in cookie):
						coords = cookie['geocode'].value
						coords = coords.replace(' ', '')
						region = cookie['region'].value
						isCookieSet = True
		template_values = {
						'coords' : coords,
						'region' : region,
						'isCookieSet' : isCookieSet,
						}
		self.response.out.write(template.render(self.path,template_values))

application = webapp.WSGIApplication([('/apis/videos.html', VideosPage)],debug = True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()
