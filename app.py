import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
import requests
import bs4
from datetime import datetime, timedelta
import os
try:
	from keys import *
except:
	HERE_APP_ID = os.environ['HERE_APP_ID']
	HERE_APP_CODE = os.environ['HERE_APP_CODE']
from math import radians, cos, sin, asin, sqrt

HERE_URL = "https://geocoder.api.here.com/6.2/geocode.json?searchtext={0}&gen=9&app_id={1}&app_code={2}"

app = Flask(__name__, static_url_path='/static')

url = "https://devpost.com/hackathons?page={0}"

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def gen_geocode_url(address):
	return HERE_URL.format(address, HERE_APP_ID, HERE_APP_CODE)

def get_url(url):
	res = requests.get(url)
	return res

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.now()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

@app.route('/', methods=['GET'])
def index():
	return render_template("index.html")

@app.route('/test', methods=['GET'])
def testPage():
	return render_template("index1.html")

def fix_unicode(string1):
	return string1.replace("\xe2\x80\x93", "-")

def extract_datetime_from_date_range_string(dateRange):
	dateRange = fix_unicode(dateRange)
	# This means it's an actual range instead of a date
	yearVal = str(dateRange)[::-1].partition(",")[0][::-1]
	if "-" in str(dateRange):
		range1 = "{}, {}".format(dateRange.partition(" - ")[0], yearVal)
		range1 = datetime.strptime(range1, '%b %d, %Y') - timedelta(days=1)
		if len(dateRange.partition(" - ")[2].partition(",")[0]) < 3:
			rangePart = dateRange.partition(" - ")[2].partition(",")[0]
			rangePart = dateRange.partition(" - ")[0].partition(" ")[0] + " " + rangePart
		else:
			rangePart = dateRange.partition(" - ")[2].partition(",")[0]
		range2 = "{}, {}".format(rangePart, yearVal)
		range2 = datetime.strptime(range2, '%b %d, %Y') + timedelta(days=1)
	else:
		range1 = "{}, {}".format(dateRange.partition(",")[0], yearVal)
		range1 = datetime.strptime(range1, '%b %d, %Y') - timedelta(days=1)
		range2 = range1 + timedelta(days=2)
	return range1, range2

def is_ongoing(dateRange):
	a, b = extract_datetime_from_date_range_string(dateRange)
	return is_time_between(a, b)

def get_address_from_hackathon(hackathonURL):
	page = bs4.BeautifulSoup(get_url(hackathonURL).text, 'lxml')
	address = str(page.select(".location")[0]).partition('https://maps.google.com/?q=')[2].partition('"')[0]
	geocodeResponse = get_url(gen_geocode_url(address))
	return geocodeResponse.json()['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]

def pull_devpost():
	toCheck = []
	for page in [1,2,3]:
		res = requests.get(url.format(page))
		page = bs4.BeautifulSoup(res.text, 'lxml')
		listOfHackathons = page.select("a.clearfix")
		for i, val in enumerate(listOfHackathons):
			dateRange = val.select(".date-range")
			# This means there is a date range present
			if len(dateRange) != 0:
				try:
					title = val.select(".title")[0].getText().strip()
				except:
					raw_input(val)
				ongoing = is_ongoing(dateRange[0].getText())
				if ongoing == True:
					hackathonURL = str(val).partition(' href="')[2].partition('"')[0]
					if len(hackathonURL) > 0:
						toCheck.append((hackathonURL, title))
				if ongoing == False and i == len(listOfHackathons) - 1:
					return toCheck
	return toCheck

def get_nearby_hackathon(longitude, latitude):
	results = []
	for val in pull_devpost():
		url, title = val
		try:
			result = get_address_from_hackathon(url)
			lat1 = result["Latitude"]
			lat2 = latitude
			long1 = result["Longitude"]
			long2 = longitude
			info = {"title": title}
			info["distance"] = haversine(long1, lat1, long2, lat2)
			results.append(info)

		except Exception as exp:
			# print("ERROR PULLING {}".format(val))
			# print(exp)
			pass
	return sorted(results, key=lambda k: k['distance'])

@app.route('/getByLongLat', methods=['GET'])
def pullFromLongLat():
	longitude = request.args.get('long', None)
	latitude = request.args.get('lat', None)
	print longitude
	print latitude
	if latitude == None or longitude == None:
		return "None"
	longitude = round(float(longitude), 7)
	latitude = round(float(latitude), 7)
	return get_nearby_hackathon(longitude, latitude)[0]['title']
	# return render_template("index1.html")

if __name__ == '__main__':
	#print pull_devpost()
	#print get_nearby_hackathon(34.7189911, -82.306362)
	app.run(host='127.0.0.1', port=5000)