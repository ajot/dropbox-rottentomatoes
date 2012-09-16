# Include the Dropbox SDK libraries
from dropbox import client, rest, session
# import get_all_klout_scores
from encodings import hex_codec
from encodings import ascii
import httplib,urllib2
import json
import sys

def parse_json(json):
	(true,false,null) = (True,False,None) # convert to a native python object
	rotten_data = eval(json) #Parsing the json payload	
	return rotten_data

# Get your app key and secret from the Dropbox developer website
APP_KEY = 'YOUR_DROP_BOX_APP_KEY_HERE'
APP_SECRET = 'YOUR_DROPBOX_APP_SECRET_HERE'
rotten_api_key ='YOUR_ROTTEN_TOMATOES_API_KEY_HERE'

# ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
ACCESS_TYPE = 'app_folder'

sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)

request_token = sess.obtain_request_token()
path = '/Users/amitjotwani/Dropbox/Apps/My DB App'

# Make the user sign in and authorize this token
url = sess.build_authorize_url(request_token)
print "url:", url
print "Please authorize in the browser. After you're done, press enter."
raw_input()

# This will fail if the user didn't visit the above URL and hit 'Allow'
access_token = sess.obtain_access_token(request_token)

client = client.DropboxClient(sess)
print "linked account:", client.account_info()

# Retrieving movies from Rotten Tomatoes
url = "http://api.rottentomatoes.com/api/public/v1.0/lists/movies/box_office.json?limit=16&country=us&apikey=" + rotten_api_key
json = urllib2.urlopen(url).read()
rotten_data = parse_json(json)

out = open(path + '/movies.html', 'w')
f = client.get_file('/movies.html').read()
out.write('<html><h1>Top Movies (via RottenTomatoes)</h1><ul>')
print f

for movie in rotten_data['movies']:
	movie_name = movie['title']
	out.write("<li>" + movie_name + "</li>")
	
out.write('</ul></html>')
out.close()


