import urllib2
import json
import logging
import os
import zipfile

class BetaSeries():

	# Init your Class 
	# Need the key for the API
	# Put the verbose mode on Off
	def __init__(self,key):
		self._key = key
		self._verbose = False


	# Search in BeataSeries database with the keyword
	# Return a list with the list of shows
	def search(self,keyword):
		url = 'http://api.betaseries.com/shows/search.json?title=' + str(keyword) + '&key=' + str(self._key)
		response = urllib2.urlopen(url)
		html = response.read()
		data = json.loads(html)

		shows = []

		try:
			for i in data['root']['shows']:
				shows.append(data['root']['shows'][i]['url'])

			if self._verbose:
				for show in shows:
					print(show)

			return shows

		except Exception as err:
			logging.error('Error : ' + str(err))

	# Get Data from a Serie using url name
	# Return a dictionnary with multiple information
	def getSerie(self,show_url):
		url = 'http://api.betaseries.com/shows/display/' + str(show_url) + '.json?key=' + str(self._key)
		response = urllib2.urlopen(url)
		html = response.read()
		data = json.loads(html)

		show_info = {}

		try:
			for i in data['root']['show']:
				show_info[i] = data['root']['show'][i]

			if self._verbose:
				for info in show_info:
					print(info)

			return show_info

		except Exception as err:
			logging.error('Error : ' + str(err))

	# Get a list of subtitle		
	# Need url show, season,nb_numero and language
	def getSubtitle(self,show_url,season,nb_episode,language):
		url = 'http://api.betaseries.com/subtitles/show/' + str(show_url) + '.json?key=' + str(self._key) + '&language=' + str(language) + '&season=' + str(season) + '&episode=' + str(nb_episode)
		response = urllib2.urlopen(url)
		html = response.read()
		data = json.loads(html)

		subtitle = {}

		try:
			for i in data['root']['subtitles']:
				subtitle[i] = data['root']['subtitles'][i]

			if self._verbose:
				for info in subtitle:
					print(info)

			return subtitle

		except Exception as err:
			logging.error('Error : ' + str(err))

	# Dowload a subtitle and extract it in a folder
	# Need a subtitle_object
	def dowloadSubtitle(self,subtitle_object):
		url = subtitle_object['url']
		name = subtitle_object['file']

		if self._verbose:
			print("downloading " + str(url))

		f = urllib2.urlopen(url)
		# Open our local file for writing
		with open(os.path.basename(name), "wb") as local_file:
			local_file.write(f.read())

		# Create a ZipFile object
		# Only 1 file per Zip
		zf = zipfile.ZipFile(name)
		zf.extract(zf.namelist()[0])


