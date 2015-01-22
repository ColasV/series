__author__ = 'vignesn'
__package__ = 'betaseries'

# import
import requests
import zipfile
import tarfile
import os
from lib.betaseries_exception import ConnectionError

# Const
BS_URL = 'https://api.betaseries.com'
VERSION = 'v=2.3'


def convert(input):
    """
    This simple function encode a string,dict or list with utf-8 and return a string

    Args:
        input (dict|list|str): an input to convert
    Returns:
        (dict|list|str) return the converted object

    """
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.items()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    else:
        return input


def json_decode(url):
    r = requests.get(url)
    json = r.json()

    return json


def extension(filename):
    try:
        t = filename.split('.')
        if len(t) == 1:
            return None
        return t[-1]
    except Exception:
        return None


class BetaSeries(object):
    """
    Singleton BetaSeries object, represent the connection to BetaSeries
    """
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = object.__new__(cls)
        return cls.instance

    def __init__(self):
        self._key = None

    def set_key(self, key):
        if not BetaSeries._verify_connection(key):
            raise ConnectionError('Incorrect key')
        self._key = key

    def get_key(self):
        if not self._key:
            raise ConnectionError('No valid key enter')
        return self._key

    @staticmethod
    def _verify_connection(key):
        url = 'https://api.betaseries.com/shows/display?id=1&key=' + str(key)

        return requests.get(url).status_code == 200

    key = property(fset=set_key, fget=get_key)


class Show():
    """
    Represent a Show
    """
    b = BetaSeries()

    def __init__(self, data):
        self.data = data
        self._episodes = self._get_episodes()

    @staticmethod
    def search(keyword):
        url = BS_URL + '/shows/search?' + VERSION + '&key=' + Show.b.key + '&title=' + keyword
        r = requests.get(url)
        json = r.json()

        list_shows = []

        for i in json['shows']:
            list_shows.append(Show(i))

        return list_shows

    def _get_episodes(self):
        url = BS_URL + '/shows/episodes?' + VERSION + '&key=' + Show.b.key + '&id=' + str(self.data['id'])
        json = json_decode(url)

        list_episodes = []

        for i in json['episodes']:
            list_episodes.append(Episode(i))

        return list_episodes

    def get_episode(self, season_nb=1, episode_nb=1):
        for episode in self._episodes:
            if episode.data.get('season') == season_nb and episode.data.get('episode') == episode_nb:
                return episode

        return None

    def __str__(self):
        return self.data.get('title')

    def __repr__(self):
        return 'Show : ' + str(self)


class Episode():

    b = BetaSeries()

    def __init__(self, data):
        self.data = data

    def _get_subtitles(self):
        url = BS_URL + '/subtitles/episode?' + VERSION + '&key=' + Episode.b.key + '&id=' + str(self.data['id'])
        json = json_decode(url)

        list_subtitle = []

        for subtitle in json['subtitles']:
            list_subtitle.append(Subtitle(subtitle))

        return list_subtitle

    def __str__(self):
        return self.data.get('title')

    def __repr__(self):
        return 'Episode : ' + str(self)


class Subtitle(object):

    b = BetaSeries()

    def __new__(cls, *args, **kwargs):
        if type(args[0]) is tuple:
            return object.__new__(cls)

        if extension(args[0]['file']) == 'zip':
            return SubtitleZip.__new__(SubtitleZip, args, kwargs)
        elif extension(args[0]['file']) == 'tar':
            return SubtitleTar.__new__(SubtitleTar, args, kwargs)
        else:
            return object.__new__(cls)

    def __init__(self, data):
        self.data = data
        self._download = False

    def download(self):
        url = self.data['url']

        r = requests.get(url)
        f = r.content

        with open(self.data['file'], "wb") as local_file:
                local_file.write(f)

        self._download = True

    def _extract(self):
        pass

    def extract(self):
        if not self._download:
            self.download()

        self._extract()


class SubtitleZip(Subtitle):
    def _extract(self):
        fh = open(self.data['file'], 'rb')
        z = zipfile.ZipFile(fh)
        for name in z.namelist():
            out_path = '.'
            z.extract(name, out_path)
        fh.close()

        os.remove(self.data['file'])


class SubtitleTar(Subtitle):
    def _extract(self):
        try:
            tar_f = tarfile.open(os.path.join(self.data['file']))
            tar_f.extractall()
            tar_f.close()
        except Exception as err:
            raise Exception(self.data['file'])


class Character():
    pass
