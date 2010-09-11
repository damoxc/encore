#
# encore/backend/medialibrary/video.py.py
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

from encore.config import config
from encore.constants import VIDEO_STREAM
from encore.interfaces import IVideoProvider, IPlayable, implements
from encore.model import *

class VideoLibrary(object):
    """
    Interface to Encores TV Show and Movie cache.
    """

    implements(IVideoProvider)


class VideoItem(object):
    """
    Class for playing video files.
    """

    implements(IPlayable)

    def __init__(self):
        super(VideoItem, self).__init__()
        self._title = ''
        self.filename = ''
        self.art_hash = ''

    @property
    def title(self):
        return self._title or self.filename

    @title.setter
    def title(self, value):
        self._title = title

    @property
    def thumbmail_uri(self):
        """
        Get the path to the thumbnail or a default.
        """
        thumb = os.path.join(config.VIDEO_THUMB_DIR, self.art_hash + '.jpg')
        if os.path.exists(thumb):
            return thumb
        else:
            return os.path.join(config.theme_path,
                'images/default_movie_art.png')

    def has_thumbnail(self):
        """
        Test if there is a thumbnail.
        """
        return os.path.exists(os.path.join(config.VIDEO_THUMB_DIR,
            self.art_hash + '.jpg'))

    # Implement IPlayable interface
    def get_title(self):
        return self.title

    def get_type(self):
        return VIDEO_STREAM

    def get_uri(self):
        return 'file://' + self.filename

class VideoItemWithMetadata(VideoItem):
    """
    Representation of a video file that has metadata linked to it.
    """

    def __init__(self):
        super(MovieItem, self).__init__()
        self.actors = []
        self.directors = []
        self.genres = []
        self.plot = ''
        self.runtime = ''
        self.short_plot = ''
        self.writers = []
        self.rating = 0
        self.year = 2000

class MovieItem(VideoItemWithMetadata):
    """
    Representation of a movie video file.
    """

    @property
    def cover_art_uri(self):
        """
        Get the URI to the cover art.
        """
        thumb = os.path.join(config.MOVIE_ART_DIR, self.art_hash + '.jpg')
        if os.path.exists(thumb):
            return thumb
        else:
            return os.path.join(config.theme_path,
                'images/default_movie_art.png')

    def has_cover_art(self):
        """
        Test if there is cover art in the cache.
        """
        return os.path.exists(os.path.join(config.MOVIE_ART_DIR,
            self.art_hash + '.jpg'))

class TVSeries(object):
    """
    TVSeries constains TVEpisodes organized by seasons.
    """

    def __init__(self, title):
        self.episode_count = 0
        self.seasons = []
        self.title = title

    @property
    def cover_art_uri(self):
        """
        Get the URI to the cover art
        """
        thumb = os.path.join(config.MOVIE_ART_DIR, self.art_hash + '.jpg')
        if os.path.exists(thumb):
            return thumb
        else:
            return os.path.join(config.theme_path,
                'images/default_movie_art.png')

    def has_cover_art(self):
        """
        Test if there is cover art in the cache.
        """
        return os.path.exists(os.path.join(config.MOVIE_ART_DIR,
            self.art_hash + '.jpg'))

class TVEpisode(VideoItemWithMetadata):
    """
    Repsentation of a TV show episode.
    """

    def __init__(self):
        super(TVEpisode, self).__init__()
        self.number = 0
