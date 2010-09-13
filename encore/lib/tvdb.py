#
# encore/lib/tvdb.py
#
# Copyright (C) 2010 Damien Churchill <damoxc@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, write to:
#   The Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor
#   Boston, MA    02110-1301, USA.
#

import os
import zlib
import hashlib
import logging
import tempfile

from twisted.web import client
from twisted.internet import defer
from twisted.internet.error import TCPTimedOutError

from xdg.BaseDirectory import xdg_cache_home
from xml.etree import cElementTree

TVDB_URL = 'http://www.thetvdb.com'

log = logging.getLogger(__name__)

class TvDbError(Exception):
    pass

class SeriesNotFoundError(TvDbError):
    pass

class EpisodeNotFoundError(TvDbError):
    pass

class TvDbResponse(object):

    def __init__(self, tvdb, data=None):
        self._data = data or {}
        self._tvdb = tvdb

    def __getattr__(self, key):
        if key in self._data:
            return self._data[key]

        # Throw an attribute error
        raise AttributeError("'%s' object has no attribute '%s'" % (
            self.__class__.__name__, key))

class Series(TvDbResponse):
    
    def __getitem__(self, season):
        if isinstance(season, int) and season >= 1:
            return Season(self, season)
        raise IndexError('list index out of range')

class Season(object):
    
    def __init__(self, series, season):
        self.series = series
        self._tvdb = series._tvdb
        self.season = season

    @property
    def poster(self):
        if not self.banners:
            return None
        return self.banners[0]

    def get_banners(self):
        return self._tvdb.get_banners(self.series.id).addCallback(
            self._got_banners)

    def _got_banners(self, banners):
        self.banners = [b for b in banners if b.season == self.season]
        return self.banners

    def get_episode(self, episode):
        return self._tvdb.get_episode(self.series.id, self.season, episode)

class Episode(TvDbResponse):
    pass

class Banner(TvDbResponse):

    @property
    def _retry_limit(self):
        return self._tvdb.retry_limit
    
    @property
    def season(self):
        if 'season' in self._data:
            return self._data['season']
        return None

    def download(self, destination, count=0):
        url = '%s/banners/%s' % (TVDB_URL, self.bannerpath)
        return client.downloadPage(url, destination).addErrback(
            self._on_download_err, destination, count)

    def _on_download_err(self, failure, destination, count):
        if failure.type is TCPTimedOutError and count < self._retry_limit:
            return self.download(destination, count + 1)
        return failure


class TvDb(object):

    def __init__(self, api_key, language='en', retry_limit=3):
        self.api_key = api_key
        self.language = language
        self.retry_limit = retry_limit

        self.cache_dir = os.path.join(xdg_cache_home, 'encore', 'tvdb')
        if not os.path.isdir(self.cache_dir):
            os.makedirs(self.cache_dir)

    @property
    def api_url(self):
        return '%s/api/%s/' % (TVDB_URL, self.api_key)

    def _on_api_error(self, failure, url, count):
        if failure.type is TCPTimedOutError and count < self.retry_limit:
            return self._request(url, count + 1)
        return failure

    def _on_api_response(self, response, url, count):
        # FIXME: Write a new Twisted HTTP downloader that supports gzip
        # decompression. This is hacky and waste of resources.
        try:
            decompress = zlib.decompressobj(zlib.MAX_WBITS + 32)
            response = zlib.decompress(response)
        except zlib.error:
            pass

        url_hash = hashlib.sha1(url).hexdigest()
        cache_path = os.path.join(self.cache_dir, url_hash) + '.xml'
        try:
            open(cache_path, 'w').write(response)
        except IOError as e:
            log.exception(e)
        return response

    def _request(self, url, count=0):
        log.debug("requesting '%s', count is %d", url, count)

        # Attempt to get the information from the cache
        url_hash = hashlib.sha1(url).hexdigest()
        cache_path = os.path.join(self.cache_dir, url_hash) + '.xml'

        if os.path.isfile(cache_path):
            d = defer.Deferred()
            d.callback(open(cache_path).read())
            return d

        return client.getPage(url).addCallbacks(
            self._on_api_response,
            self._on_api_error,
            callbackArgs=(url, count),
            errbackArgs=(url, count)
        )

    def get_languages(self):
        """
        Return the supported languages by the tvdb
        """
        return self._request(self.api_url + 'languages.xml').addCallback(
            self._on_got_languages)

    def _on_got_languages(self, langs):
        etree = cElementTree.fromstring(langs)
        languages = []
        for elm in etree:
            lang = {}
            for key in elm:
                lang[key.tag] = key.text
            languages.append(lang)
        return languages

    def get_mirrors(self):
        """
        Fetch the list of mirrors that can be used to gather data from
        thetvdb.org.
        """

        return client.getPage(self.api_url + 'mirrors.xml').addCallbacks(
            self._on_got_mirrors,
            self._on_api_error
        )

    def _on_got_mirrors(self, result):
        pass

    def get_series(self, series):
        """
        Get a series object by its name.

        :param series: The series name to look for
        :type series: str
        """
        series = series.replace(' ', '+')
        url = '%s/api/GetSeries.php?seriesname=%s' % (TVDB_URL, series)
        return self._request(url).addCallback(
            self._on_got_series, series)

    def _on_got_series(self, results, series_name):
        etree = cElementTree.fromstring(results)

        # Check to see if any series were found
        if not etree:
            raise SeriesNotFoundError("Cannot find '%s'", series_name)

        # Get the first match
        series = None
        for elm in etree:
            series = dict([(k.tag.lower(), k.text) for k in elm])
            break

        # Ensure that there has been a match
        if not series:
            raise SeriesNotFoundError("Cannot find '%s'", series_name)

        return self.get_series_by_id(series['id'])

    def get_series_by_id(self, series_id):
        """
        Get a series object by its id.

        :param series_id: The series id to fetch
        :type series_id: int
        """

        url = self.api_url + 'series/%s/%s.xml' % (series_id, self.language)
        return self._request(url).addCallback(
            self._on_got_series_details)

    def _on_got_series_details(self, results):
        etree = cElementTree.fromstring(results)

        # Check to see if any series were found
        if not etree:
            raise SeriesNotFoundError

        data = dict([(k.tag.lower(), k.text) for k in etree.find('Series')])
        return Series(self, data)

    def get_banners(self, series_id):
        """
        Get the banners for the specified series.

        :param series_id: The id for the series to fetch the banners for
        :type series_id: int
        """

        url = self.api_url + 'series/%s/banners.xml' % series_id
        return self._request(url).addCallback(
            self._on_got_banners)

    def _on_got_banners(self, response):
        etree = cElementTree.fromstring(response)

        banners = []
        for elm in etree:
            data = dict([(k.tag.lower(), k.text) for k in elm])
            if 'season' in data:
                data['season'] = int(data['season'])
            banners.append(Banner(self, data))
        return banners

    def get_episode(self, series_id, season, episode):
        """
        Get the data for the specified episode.

        :param series_id: The id of the series that the episode is of
        :type series_id: int
        :param season: The season number
        :type season: int
        :param episode: The episode numbe
        :type episode: int
        """
        url = self.api_url + 'series/%s/default/%s/%s/%s.xml' % (
            series_id, season, episode, self.language)
        return self._request(url).addCallback(
            self._on_got_episode)

    def _on_got_episode(self, response):
        etree = cElementTree.fromstring(response)

        # Check to see if any series were found
        if not etree:
            raise EpisodeNotFoundError

        data = dict([(k.tag.lower(), k.text) for k in etree.find('Episode')])
        return Episode(self, data)
