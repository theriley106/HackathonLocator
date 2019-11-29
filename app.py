import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
import requests
import bs4
from datetime import datetime, timedelta

app = Flask(__name__, static_url_path='/static')

url = "https://devpost.com/hackathons"

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
	print(str(dateRange))
	yearVal = str(dateRange)[::-1].partition(",")[0][::-1]
	if "-" in str(dateRange):
		range1 = "{}, {}".format(dateRange.partition(" - ")[0], yearVal)
		range1 = datetime.strptime(range1, '%b %d, %Y') - timedelta(days=1)
		range2 = "{}, {}".format(dateRange.partition(" - ")[2].partition(",")[0], yearVal)
		range2 = datetime.strptime(range2, '%b %d, %Y') + timedelta(days=1)
	else:
		range1 = "{}, {}".format(dateRange.partition(",")[0], yearVal)
		range1 = datetime.strptime(range1, '%b %d, %Y') - timedelta(days=1)
		range2 = range1 + timedelta(days=2)
	return range1, range2

def is_ongoing(dateRange):
	a, b = extract_datetime_from_date_range_string(dateRange)
	return is_time_between(a, b)

def pull_devpost():
	res = requests.get(url)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	listOfHackathons = page.select(".clearfix")

	for val in listOfHackathons:
		dateRange = val.select(".date-range")
		# This means there is a date range present
		if len(dateRange) != 0:
			print is_ongoing(dateRange[0].getText())
			# extract_datetime_from_date_range_string(dateRange[0].getText())
			# raw_input()
	print page.title.string

def get_nearby_hackathon(longitude, latitude):
	return

@app.route('/getByLongLat', methods=['GET'])
def pullFromLongLat():
	longitude = request.args.get('long', None)
	latitude = request.args.get('lat', None)
	if latitude == None or longitude == None:
		return "None"
	return render_template("index1.html")

if __name__ == '__main__':
	pull_devpost()
	# app.run(host='127.0.0.1', port=5000)