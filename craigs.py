import pandas as pd
# %pylab inline
import requests
from bs4 import BeautifulSoup as bs4
url_base = 'http://raleigh.craigslist.org/search/ggg'
params = dict()
rsp = requests.get(url_base, params=params)
print(rsp.url)
print(rsp.text[:500])

# BS4 can quickly parse our text, make sure to tell it that you're giving html
html = bs4(rsp.text, 'html.parser')

# BS makes it easy to look through a document
print(html.prettify()[:1000])

# find_all will pull entries that fit your search criteria.
# Note that we have to use brackets to define the `attrs` dictionary
# Because "class" is a special word in python, so we need to give a string.
gigs = html.find_all('p', attrs={'class': 'row'})
print(thisGig.prettify())

class Gig:
	def __init__(self, name):
		self.name = name

allGigs = []
for gig in gigs:
	allGigs.append(Gig(gig.findAll(attrs={'class': 'hdrlnk'})[0].text))
print(len(allGigs))