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
		print(self.name + ' ~ ' + self.url)
		params = dict()
		rsp = requests.get(self.url, params=params)
		# BS4 can quickly parse our text, make sure to tell it that you're giving html
		html = bs4(rsp.text, 'html.parser')
		self.datetime = 'unknown'
		if len(html.find_all(datetime=True)) > 0:
			self.datetime = html.find_all(datetime=True)[0]['datetime']
		links = html.find_all(href=True)
		self.lon = 'unknown'
		self.lat = 'unknown'
		for link in links:
			if 'maps.google.com/maps/preview' in link['href']:
				if len(link['href'].split('@')) > 0:
					longlat = link['href'].split('@')[1].split(',')
					self.lon = longlat[0]
					self.lat = longlat[1]
				break
		self.about = 'unknown'
		if len(html.findAll(attrs={'id': 'postingbody'})) > 0:
			if len(html.findAll(attrs={'id': 'postingbody'})[0].text.split('QR Code Link to This Post')) > 0:
				self.about = html.findAll(attrs={'id': 'postingbody'})[0].text.split('QR Code Link to This Post')[1].lstrip().replace(',','').replace('\n', '   ')
			else:
				self.about = html.findAll(attrs={'id': 'postingbody'})[0].text.lstrip().replace(',','').replace('\n', '   ')
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
		self.pay = 'Unknown'
		if len(html.findAll(attrs={'class': 'attrgroup'})) > 0:
			compsection = html.findAll(attrs={'class': 'attrgroup'})[0]
			# self.pay = compsection
			if compsection.find('b'):
				self.pay = compsection.find('b').text


def getAllGigsEverywhere():
	allGigs = []
	locations = []
	with open('locs.txt') as f:
		locations = f.read().splitlines()
	count = 0
	for loc in locations:
		print(count)
		count += 1
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
			if not '.craigslist.' in gigUrl:
				gigUrl = loc_url + gigUrl
			elif not 'http:' in gigUrl:
				gigUrl = 'http:' + gigUrl
			myGig = Gig(gig.findAll(attrs={'class': 'hdrlnk'})[0].text, loc, gigUrl)
			myGig.getInfoFromCraig()
			allGigs.append(myGig)
	return allGigs

f = open('nearnc.csv','w')
count = 0
f.write(('Name,Location,URL,datetime,lon,lat,genre,pay,about' + '\n').encode('utf-8'))
for gig in getAllGigsEverywhere():
	print(count)
	count += 1
	if gig.lon is 'unknown':
		continue
	line = gig.name + ',' + gig.location + ',' + gig.url + ',' + gig.datetime + ',' + gig.lon + ',' + gig.lat + ',' + gig.genre + ',' + gig.pay + ',' + gig.about
	f.write((line + '\n').encode('utf-8'))
f.close()