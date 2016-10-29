import pandas as pd
# %pylab inline
import requests
from bs4 import BeautifulSoup as bs4

class Gig:
	def __init__(self, name, location, url):
		self.name = name
		self.location = location
		self.url = url

	def getInfoFromCraig(self):
		params = dict()
		rsp = requests.get(self.url, params=params)
		# BS4 can quickly parse our text, make sure to tell it that you're giving html
		html = bs4(rsp.text, 'html.parser')
		self.datetime = html.find_all(datetime=True)[0]['datetime']
		links = html.find_all(href=True)
		for link in links:
			if 'maps.google' in link['href']:
				longlat = link['href'].split('@')[1].split(',')
				self.lon = longlat[0]
				self.lat = longlat[1]
		self.about = html.findAll(attrs={'id': 'postingbody'})[0].text.split('QR Code Link to This Post')[1].lstrip()
		if 'lbg' in self.url:
			self.genre = 'labor'
		elif 'cpg' in self.url:
			self.genre = 'computer'
		elif 'crg' in self.url:
			self.genre = 'creative'
		elif 'cwg' in self.url:
			self.genre = 'crew'
		elif 'dmg' in self.url:
			self.genre = 'domestic'
		elif 'evg' in self.url:
			self.genre = 'event'
		elif 'tlg' in self.url:
			self.genre = 'talent'
		elif 'wrg' in self.url:
			self.genre = 'writing'
		else:
			self.genre = 'other'
		compsection = html.findAll(attrs={'class': 'attrgroup'})[0]
		self.pay = compsection.find('b').text


def getAllGigsEverywhere():
	allGigs = []
	locations = []
	with open('craigsLocations.txt') as f:
		locations = f.read().splitlines()
	count = 0
	for loc in locations:
		count += 1
		if count > 2:
			break
		loc_url = 'http://' + loc + '.craigslist.org'
		url_base = loc_url + '/search/ggg'
		params = dict()
		rsp = requests.get(url_base, params=params)

		# BS4 can quickly parse our text, make sure to tell it that you're giving html
		html = bs4(rsp.text, 'html.parser')

		# find_all will pull entries that fit your search criteria.
		# Note that we have to use brackets to define the `attrs` dictionary
		# Because "class" is a special word in python, so we need to give a string.
		gigs = html.find_all('p', attrs={'class': 'row'})
		for gig in gigs:
			gigUrl = gig.find_all(href=True)[0]['href']
			allGigs.append(Gig(gig.findAll(attrs={'class': 'hdrlnk'})[0].text, loc, loc_url + gigUrl))
	return allGigs

print(getAllGigsEverywhere()[0].getInfoFromCraig())