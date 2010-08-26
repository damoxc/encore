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
from encore.lib.tvdb import Tvdb

# The TV DB key
TVDB_KEY = '5B4FABAEAB3DAB49'

# The Movie DB key
TMDB_KEY = '9b41e54a1df985e5d9e90cab7646e5ca'

# Configure the moviedb api
tmdb_config['key'] = TMDB_KEY

# Configure the tvdb api
TvDb = Tvdb(apikey=TVDB_KEY)

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
    filename = os.path.basename(path)
    filename = os.path.splitext(filename)[0]

    # Strip .,-_ from the filename
    for item in TITLE_STRIP_SEARCH:
        filename = filename.replace(item, ' ')

    # Split title at keywords
    for item in TITLE_SPLIT_KEYWORDS:
        filename = filename.split(item)[0]
    filename = filename.strip()

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

class MetadataSearchBase(object):
    """
    Base class for both the SeriesMetadataSearch and MovieMetadataaSearch
    that allows Encore to gather additional information about videos.
    """
    
    def get_metadata(self):
        raise NotImplementedError
