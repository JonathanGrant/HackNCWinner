import csv

pornwords = []
with open("pornwords.txt", "r") as ins:
	for line in ins:
		pornwords.append(line.rstrip('\n'))

class Gig:
	def __init__(self, name, location, url, datetime, lon, lat, genre, pay, about):
		self.name = name
		self.location = location
		self.url = url
		self.datetime = datetime
		self.lon = lon
		self.lat = lat
		self.genre = genre
		self.pay = pay
		self.about = about
		self.pornpoints = 0
		self.isPorn = False

	def getPornoScore(self):
		for word in pornwords:
			if word in self.about:
				self.pornpoints += 5
			if word in self.name:
				self.pornpoints += 30
		if (len(self.name) + len(self.about)) > 0:
			self.pornpercent = (1.0 * self.pornpoints / (len(self.name) + len(self.about)))
		else:
			self.pornpercent = 0
		if self.pornpercent > 0.25:
			self.pornlevel = 2
		elif self.pornpercent > 0:
			self.pornlevel = 1
		else:
			self.pornlevel = 0

gigs = []
count = 0
f = open('nearncporn.csv','w')
f.write(('Name,Location,URL,datetime,lon,lat,genre,pay,about,pornpoints,pornpercent,pornlevel' + '\n').encode('utf-8'))
with open("nearnc.csv", "rU") as ff:
	reader = csv.reader(ff, delimiter="\n",dialect=csv.excel_tab)
	for i, line in enumerate(reader):
		count += 1
		print count
		fields = line[0].split(',')
		myGig = Gig(fields[0],fields[1],fields[2],fields[3],fields[4],fields[5],fields[6],fields[7],fields[8])
		gigs.append(myGig)
		if myGig.lon is 'unknown':
			continue
		myGig.getPornoScore()
		line = myGig.name + ',' + myGig.location + ',' + myGig.url + ',' + myGig.datetime + ',' + myGig.lon + ',' + myGig.lat + ',' + myGig.genre + ',' + myGig.pay + ',' + myGig.about + ',' + str(myGig.pornpoints) + ',' + str(myGig.pornpercent) + ',' + str(myGig.pornlevel)
		f.write((line + '\n'))
f.close()



