import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import bs4
import requests
import os



URL = "https://devpost.com/software/search?page={0}&query=is%3Awinner"

if __name__ == '__main__':
	for i in range(1, 625):
		url = URL.format(i)
		res = requests.get(url)
		print("{} {} {}".format(i, url, len(res.text)))
		with open('files/{}.html'.format(i), 'w') as f:
		    f.write(res.text)