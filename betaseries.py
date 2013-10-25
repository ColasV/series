import urllib2
import json
import logging
import os
import zipfile
import string
import collections

from datetime import date

# Const
BS_URL = 'http://api.betaseries.com'
SUB_EN = 'VO'
SUB_FR = 'VF'


# Utilities function
def convert(input):
	"""
	This simple function encode a string,dict or list with utf-8 and return a string

	Args:
		input (dict|list|str): an input to convert
	Returns:
		(dict|list|str) return the converted object

	"""
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

		return content 

	description = property(_get_description)
	title = property(_get_title)
	date = property(_get_date)

class Show():
	"""
	Class Show

	Show object allow you to interact with show informations.

	Args:
		show_info (str): A valid show url string


	.. note::
		You are not suppose to create a Show object, the main class is supose to do that.

	"""
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
		content += 'Duration : ' + self.duration

		return convert(content) 


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
	
	name = property(_get_name)

# Class SubtitleZip
# Sub-Class from Subtitle which is used for extracting zip or tar.gz
class SubtitleZip(Subtitle):
	"""
	Class SubtitleZip : sub-class from Subtitle


	"""

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


class SubtitleTar(Subtitle):
	"""
	Class SubtitleTar

	"""

	def download(self,path=None):
		return None




class BetaSeries():
	"""

	Class BetaSeries : The main class of the library

	BetaSeries Object allow you to interact with the BetaSeries API

	Args:
		key (str): Key API, you can get in one from http://www.betaseries.com


	To create a new instance it's very easy:
	
	>>> import betaseries
	>>> betaseries.BetaSeries('a23736dhbee')

	"""


	def __init__(self,key):
		self._key = key
		self._verbose = False

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


	def search_keyword(self,keyword):
		"""

		This function search a keyword in the BetaSeries database.

		The function search all the occurence of the keyword in the database.

		Args:
			Keyword : A string keyword

		Returns:
			Return a list which contain all the occurence find in the database

			Each element contain a dict element with two keys :
				url : contain the url show 
				title : title of the show

		"""
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

	
	def search(self,keyword,case_sensitive=False):
		"""

		This function search a specific keyword in the BetaSeries database.

		The function search the exact occurence in the database.

		Args:
			Keyword (str): A string keyword
			case_sensitive: Allow you to search with or without case senstive 

		Returns:
			Return a namedtuple which contain two informations:
				url : contain the url show.
				title : title of the show.

			You can easily access to this two attributs:
				response.url
				response.url

		"""

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

	def get_show(self,show_url):
		"""

		This function get show informations. Need a valid show url.

		Args:
			show_url (str): A valid show url string

		Returns:
			Return a Show object

			You can easily access to these information by looking in the Show class

		"""

		try:
			url = BS_URL + '/shows/display/' + str(show_url) + '.json?key=' + str(self._key)
			data = self._decode_json(url)

			show = Show(data['root']['show'])

			if self._verbose:
				logging.info('*Show object correctly created')

			return show

		except Exception as err:
			logging.error('Error : ' + str(err))

	
	def get_subtitle(self,show_url,season,episode,language=SUB_EN):
		"""

		This function get a list of subtitle

		Args:
			show_url (str): A valid show url string.
			season (int): season number.
			episode (int): episode number.
			language (str): (Optionnal default = SUB_EN) The type of subtitle english or french version

		Returns:
			Return a list of Subtitle object

			You can easily access to these subtitles by looking in the Subtitle object

		"""
		try:

			url = BS_URL + '/subtitles/show/' + str(show_url) + '.json?key=' + str(self._key) + '&language=' + str(language) + '&season=' + str(season) + '&episode=' + str(episode)
			data = self._decode_json(url)

			subtitles = []

			for i in data['root']['subtitles']:
				extension = data['root']['subtitles'][i]['file'].split(".")
				
				# Check the differente extensio, can be zip file or srt file.
				if (extension[-1] == 'zip'):
					subtitles.append(SubtitleZip(data['root']['subtitles'][i]))
				else:
					subtitles.append(Subtitle(data['root']['subtitles'][i]))

			if self._verbose:
				for info in subtitles:
					print(info)

			return subtitles

		except Exception as err:
			logging.error('Error : ' + str(err))


	def get_episode(self,show_url,season,episode):
		"""

		This function get episode informations.

		Args:
			show_url (str): A valid show url string.
			season (int): A season number.
			episode (int): An episode number

		Returns:
			Return an Episode object

			You can easily access to these information by looking in the Episode class

		"""
		try:
			url = BS_URL + '/shows/episodes/' + str(show_url) + '.json?key=' + str(self._key) + '&season=' + str(season) + '&episode=' + str(episode)
			data = self._decode_json(url)

			episode = Episode(data['root']['seasons']['0']['episodes']['0'])

			return episode

		except Exception as err:
			logging.error('Error : ' + str(err))
