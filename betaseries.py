# Important stuff

import urllib2
import json
import logging
import os
import zipfile
import string
import collections

from datetime import date

BS_URL = 'http://api.betaseries.com'
SUB_EN = 'VO'
SUB_FR = 'VF'


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

# Class Episode
# Object is using by the BS class
# Contain all the informations about 1 episode
class Episode():

	def __init__(self,episode_info):
		self._episode_info = episode_info
	
	def _get_title(self):
		return self._episode_info['title']

	def _get_date(self):
		date_object = date.fromtimestamp(self._episode_info['date'])
		return date_object.strftime("%A %d. %B %Y")

	def _get_description(self):
		return convert(self._episode_info['description'])

	def __str__(self):
		content = 'Title : ' + self.title + '\n'
		content += 'Date : ' + self.date + '\n'
		content += 'Description : ' + self.description

		return content 

	description = property(_get_description)
	title = property(_get_title)
	date = property(_get_date)

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

	def __str__(self):
		content = 'Title : ' + self.title + '\n'
		content += 'Description : ' + self.description

		return content 


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

	def download(self,path=None):
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
			zf.extract(zf.namelist()[0],path)

			# Delete the zip file after that
			os.remove(name)

			# return the file nane
			return zf.namelist()[0]
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


	# Decode a JSON url
	# Check if no error are raised by the API
	def _decode_json(self,url):
		try:
			response = urllib2.urlopen(url)
			html = response.read()
			data = json.loads(html)
		except Exception as err:
			logging.error('Error during parsing : ' + str(err))
		
		if 'code' in data['root']:
			if data['root']['code'] != 1:
				raise Exception('Error with the API, code : ' + str(data['root']['code']))	


		return data


	# Search in BeataSeries database with the keyword
	# Return a list with a list of shows
	def search_keyword(self,keyword):
		keyword = keyword.split(" ")
		keyword = "_".join(keyword)
		try:
			url = BS_URL + '/shows/search.json?title=' + str(keyword) + '&key=' + str(self._key)
			data = self._decode_json(url)
		
			shows = []
		
			for i in data['root']['shows']:
				shows.append(data['root']['shows'][i])

			if self._verbose:
				for show in shows:
					print(show)

			return shows

		except Exception as err:
			logging.error('Error : ' + str(err))

	# Search a specific keyword in the database
	# Case_sensitive allow you to be more specific
	def search(self,keyword,case_sensitive=False):
		show_result = collections.namedtuple('show_result', ['url', 'title'])

		out = self.search_keyword(keyword)

		if not case_sensitive:
			keyword = string.lower(keyword)

		for i in out:
			title = i['title']
			if not case_sensitive:
				title = string.lower(title)

			if  title == keyword:
				return show_result(i['url'],i['title'])

		return None


	# Get Data from a Serie using url name
	# Return a Show object
	def get_show(self,show_url):
		try:
			url = BS_URL + '/shows/display/' + str(show_url) + '.json?key=' + str(self._key)
			data = self._decode_json(url)

			show = Show(data['root']['show'])

			if self._verbose:
				logging.info('*Show object correctly created')

			return show

		except Exception as err:
			logging.error('Error : ' + str(err))

	# Get a list of subtitle object	
	# Need url show, season,nb_numero and language
	# Language = (SUB_FR|SUB_EN)
	def get_subtitle(self,show_url,season,episode,language=SUB_EN):
		try:

			url = BS_URL + '/subtitles/show/' + str(show_url) + '.json?key=' + str(self._key) + '&language=' + str(language) + '&season=' + str(season) + '&episode=' + str(episode)
			data = self._decode_json(url)

			subtitles = []

			for i in data['root']['subtitles']:
				subtitles.append(Subtitle(data['root']['subtitles'][i]))

			if self._verbose:
				for info in subtitles:
					print(info)

			return subtitles

		except Exception as err:
			logging.error('Error : ' + str(err))


	# Get informations about 1 episode
	# Need show_url, season number and episode number
	# return an Episode object
	def get_episode(self,show_url,season,episode):
		try:
			url = BS_URL + '/shows/episodes/' + str(show_url) + '.json?key=' + str(self._key) + '&season=' + str(season) + '&episode=' + str(episode)
			data = self._decode_json(url)

			episode = Episode(data['root']['seasons']['0']['episodes']['0'])

			return episode

		except Exception as err:
			logging.error('Error : ' + str(err))
