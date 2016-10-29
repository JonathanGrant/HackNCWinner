var express = require('express');
var app = express();
var path = require('path');
var fs = require('fs');

app.use("/", express.static(__dirname + '/'));

app.get('/', function(req, res) {
  res.sendFile(path.join(__dirname + '/index.html'))
});

app.get('/alllocations', function(req, res) {
	fs.readFile('craigsLocations.txt', 'utf8', function (err,data) {
		if (err) {
			console.log(err);
			return err
		}
		res.send(data)
	})
})

app.get('/allgigs', function(req, res) {
	fs.readFile('gigs.txt', 'utf8', function (err,data) {
		if (err) {
			console.log(err);
			return err
		}
		console.log(typeof data)
		res.send(data)
	})
})

app.listen(process.env.PORT || 3000);