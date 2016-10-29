import pandas as pd
# %pylab inline
import requests
from bs4 import BeautifulSoup as bs4

class Gig:
	def __init__(self, name, location):
		self.name = name
		self.location = location

allGigs = []
locations = []
with open('craigsLocations.txt') as f:
	locations = f.read().splitlines()
count = 0
for loc in locations:
	count += 1
	if count > 2:
		break
	url_base = 'http://' + loc + '.craigslist.org/search/ggg'
	params = dict()
	rsp = requests.get(url_base, params=params)

	# BS4 can quickly parse our text, make sure to tell it that you're giving html
	html = bs4(rsp.text, 'html.parser')

	# find_all will pull entries that fit your search criteria.
	# Note that we have to use brackets to define the `attrs` dictionary
	# Because "class" is a special word in python, so we need to give a string.
	gigs = html.find_all('p', attrs={'class': 'row'})
	for gig in gigs:
		allGigs.append(Gig(gig.findAll(attrs={'class': 'hdrlnk'})[0].text, loc))
print(allGigs[0].name)