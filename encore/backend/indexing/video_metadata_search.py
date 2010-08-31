#
# encore/backend/indexing/video_metadata_search.py
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
import re
from collections import namedtuple

from encore.lib.tmdb import MovieDb, config as tmdb_config
from encore.lib.tvdb import TvDb

# The TV DB key
TVDB_KEY = '5B4FABAEAB3DAB49'

# The Movie DB key
TMDB_KEY = '9b41e54a1df985e5d9e90cab7646e5ca'

# Configure and create the moviedb api
tmdb_config['key'] = TMDB_KEY
mdb = MovieDb()

# Create the tvdb api
tvdb = TvDb(TVDB_KEY)

# Title split keywords
TITLE_SPLIT_KEYWORDS = [
    '[', ']', '~', '(', ')', 'dvdscr', 'dvdrip', 'dvd-rip', 'dvdr', 'vcd',
    'divx', 'xvid', 'ac3', 'r5', 'pal', 'readnfo', 'uncut', 'cd1', 'cd2',
    'dvdiso'
]

# Title strip items
TITLE_STRIP_SEARCH = ['.', '-', '_']

# RegExps to try and match a series filename
SERIES_FILENAME_RE = [
    re.compile(r'(?P<title>.*?)(s?)(?P<season>\d{1,2})(x|e|xe)(?P<episode>\d{1,2})'),
    re.compile(r'(?P<title>.*?)season\s(?P<season>\d{1,2})\sepisode\s(?P<episode>\d{1,2})')
]

# RegExps to try and match a series path
SERIES_PATH_RE = [
    re.compile(r'(?P<title>.*?)/[a-zA-Z]+\s+(?P<season>\d{1,2})/(?P<episode>\d{1,2})'),
    re.compile(r'(?P<title>.*?)\s*?(/|-)\s*[a-zA-Z]+\s+(?P<season>\d{1,2})/(?P<episode>\d{1,2})')
]

VideoFileInfo = namedtuple('VideoFileInfo', 'title episode season')

class VideoMetadata(object):

    def __init__(self, data=None):
        if not data:
            data = {}
        self._data = data

    def __getattr__(self, key):
        try:
            return self._data[key]
        except:
            raise AttributeError

class MovieMetadata(VideoMetadata):
    
    @property
    def poster(self):
        return self.images[0]

    @property
    def backdrop(self):
        return self.images[1]

class SeriesMetadata(VideoMetadata):

    @property
    def poster(self):
        for poster in self._banners['poster']['680x100']:
            pass
    
    def __getitem__(self, key):
        return SeasonMetadata(self._data[key])

class SeasonMetadata(VideoMetadata):

    def __getitem__(self, key):
        return EpisodeMetadata(self._data[key])

class EpisodeMetadata(VideoMetadata):
    pass

def strip_filename(filename):
    """
    This function strips out and cleans a video filename

    :param filename: The filename to strip
    :type filename: str
    :returns: The stripped filename
    :rtype: str
    """

    filename = os.path.splitext(filename)[0]

    # Strip .,-_ from the filename
    for item in TITLE_STRIP_SEARCH:
        filename = filename.replace(item, ' ')

    # Split title at keywords
    for item in TITLE_SPLIT_KEYWORDS:
        filename = filename.split(item)[0]
    return filename.strip()

def parse_path(path):
    """
    Parse the path to the video file. Parsing the whole path allows for
    multiple formats of storage:

        Prison_Break_s02e10_something.something.avi
        Prison Break/Season 2/10 something.avi
        Prison Break - Season 2/10 - something.avi

    :param path: The path of the movie
    :type path: str
    :returns: Tuple containing (title, season, episode)
    :rtype: tuple
    """

    # Lowercase path and get the filename minus extension
    path = path.lower()

    # Strip the filename
    filename = strip_filename(os.path.basename(path))

    # Search the path for the title, season and episode
    for regexp in SERIES_PATH_RE:
        match = regexp.search(path)
        if match:
            break

    if not match:
        # Search the filename for the title, season and episode
        for regexp in SERIES_FILENAME_RE:
            match = regexp.search(filename)
            if match:
                break

    if not match:
        return VideoFileInfo(
            title   = filename,
            season  = 0,
            episode = 0
        )

    # Get the information from the regexp match
    return VideoFileInfo (
        title   = os.path.basename(match.group('title')).strip(),
        season  = int(match.group('season')),
        episode = int(match.group('episode'))
    )

def get_movie_metadata(title):
    """
    Search themoviedb.org for metadata for the movie specified.

    :param title: The movie title
    :type title: str
    :returns: Information about the movie
    :rtype: MovieMetadata
    """

    results = mdb.search(title)
    for result in results:
        if title == result['name'].lower():
            break
        result = None

    if result is None:
        return

    return MovieMetadata(result)

def get_movie_info(movie_id):
    """
    Search themoviedb.org for images for the movie specified.

    :param movie_id: The moviedb.org movie id
    :type movie_id: str or int
    :returns: Detailed information about the movie
    :rtype: MovieMetadata
    """
    
    return MovieMetadata(mdb.getMovieInfo(movie_id))

def get_series_metadata(title):
    """
    Search thetvdb.org for metadata for the series specified.

    :param title: The series title
    :type title: str
    :returns: Information about the series
    :rtype: SeriesMetadata
    """

    return SeriesMetadata(tvdb[title])

def get_season_metadata(title, season):
    """
    Search thetvdb.org for metadata for the season specified.

    :param title: The series title
    :type title: str
    :param season: The season number
    :type season: int
    :returns: Information about the season
    :rtype: SeasonMetadata
    """

    return SeasonMetadata(tvdb[title][season])

def get_episode_metadata(title, season, episode):
    """
    Search thetvdb.or for metadata for the episode specified.

    :param title: The series title
    :type title: str
    :param season: The season number
    :type season: int
    :param episode: The episode number
    :type episode: int
    :returns: Information about the season
    :rtype: EpisodeMetadata
    """

    return EpisodeMetadata(tvdb[title][season][episode])
