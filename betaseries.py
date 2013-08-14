# Important stuff

import urllib2
import json
import logging
import os
import zipfile

# Utilities function

def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


# Class Show
# Object is using by the BetaSeries class
class Show():
	# Init your object
	# Need data from the show
	def __init__(self,show_info):
		self._show_info = show_info

	def _get_title(self):
		return self._show_info['title']

	def _get_description(self):
		return convert(self._show_info['description'])

	def _get_duration(self):
		return self._show_info['duration']

	def _get_banner(self):
		return self._show_info['banner']


	description = property(_get_description)
	title = property(_get_title)
	duration = property(_get_duration)
	banner = property(_get_banner)

# Class Subtitle
# Using to create subtitle object
# Allow to download the subtitle and get informations
class Subtitle():

	def __init__(self,subtitle_info):
		self._subtitle = subtitle_info

	def _get_name(self):
		return self._subtitle['file']

	def download(self):
		url = self._subtitle['url']
		name = self._subtitle['file']
		try:
			f = urllib2.urlopen(url)
			# Open our local file for writing
			with open(os.path.basename(name), "wb") as local_file:
				local_file.write(f.read())
		except Exception as err:
			logging.error('Error during downloading :' + str(err))
		try:
			# Create a ZipFile object
			# Only 1 file per Zip
			zf = zipfile.ZipFile(name)
			zf.extract(zf.namelist()[0])
		except Exception as err:
			logging.error('Error during opening archive :' + str(err))


	name = property(_get_name)



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
	def getShow(self,show_url):
		url = 'http://api.betaseries.com/shows/display/' + str(show_url) + '.json?key=' + str(self._key)
		response = urllib2.urlopen(url)
		html = response.read()
		html = html
		data = json.loads(html)

		try:
			show = Show(data['root']['show'])

			if self._verbose:
				logging.info('*Show object correctly created')

			return show

		except Exception as err:
			logging.error('Error : ' + str(err))

	# Get a dictionnaries of subtitle		
	# Need url show, season,nb_numero and language
	def getSubtitle(self,show_url,season,nb_episode,language='VO'):
		url = 'http://api.betaseries.com/subtitles/show/' + str(show_url) + '.json?key=' + str(self._key) + '&language=' + str(language) + '&season=' + str(season) + '&episode=' + str(nb_episode)
		response = urllib2.urlopen(url)
		html = response.read()
		data = json.loads(html)

		subtitles = {}

		try:
			for i in data['root']['subtitles']:
				subtitles[i] = Subtitle(data['root']['subtitles'][i])

			if self._verbose:
				for info in subtitles:
					print(info)

			return subtitles

		except Exception as err:
			logging.error('Error : ' + str(err))



