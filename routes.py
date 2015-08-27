#==================================================
#========== IMPORTING REQUIRED MODULES ============
#==================================================

from flask import Flask, render_template
from functools import wraps
import urllib2
import json
import unirest

# INIT MAIN FLASK APP
app = Flask(__name__)

#==================================================
#================= MAIN ROUTES ====================
#==================================================

#Index page route
@app.route('/')
def home():
	return render_template('form.html')

#Download page route
@app.route('/download/<id>')
def download(id):
	ALL_TITLE = [] # stores title of video
	ALL_FORMAT = [] # stores formats of video
	ALL_QUALITY = [] # stores different video qualities
	ALL_URL = [] # stores download urls of video

	# init API
	response = unirest.get("https://ytgrabber.p.mashape.com/app/get/" + id,
		headers={
		    "X-Mashape-Key": "V96M0xptiXmsh39L6Mw7CES0c7zgp1C7HOLjsnZGls6d3LiDjm",
		    "Accept": "application/json"
		}
	)
	
	data = json.dumps(response.body, separators=(',',':')) # getting json response
	vid_title = (json.loads(data))['title'] # loading json data
	ALL_TITLE.append(vid_title) # extracting TITLE of Video
	data = (json.loads(data))['link'] # list of download links of video
	
	# iterates through deifferent formats of video
	for each in data:
		vid_format = each["type"]["format"] # getting video format
		vid_quality = each["type"]["quality"] # geting video quality
		vid_url = each["url"] # geting video download url

		ALL_URL.append(str(vid_url)) # adding video download url to list
		ALL_FORMAT.append(str(vid_format)) # adding video format to list
		ALL_QUALITY.append(str(vid_quality)) # adding video quality to list

	return render_template('download.html', all_title=ALL_TITLE, all_format=ALL_FORMAT, all_quality=ALL_QUALITY, all_url=ALL_URL, id=id)

if __name__ == '__main__':
    app.run(debug=True) # run the app