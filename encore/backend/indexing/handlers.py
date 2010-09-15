#
# encore/backend/indexing/handlers.py
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

import logging

from twisted.internet import reactor, defer

from encore.config import config
from encore.backend.model import *
from encore.backend.indexing.utilities import TagGetter
from encore.backend.indexing.video_metadata import *

log = logging.getLogger(__name__)

class FileHandler(object):
    """
    Abstract class for all indexing file handlers.
    """

    def __init__(self):
        self.deferreds = {}

    def _deferred(self, filename):
        self.deferreds[filename] = defer.Deferred()
        return self.deferreds[filename]

    def _callback(self, filename, result):
        self.deferreds.pop(filename).callback(result)

    def __call__(self, filename):
        raise NotImplementedError

class VideoHandler(FileHandler):
    """
    Base-class for indexing video files.
    """

    def __call__(self, filename):
        file_info = parse_path(filename)
        if file_info.season:
            reactor.calllLater(0, self._handle_series, filename, file_info)
        else:
            reactor.callLater(0, self._handle_movie, filename, file_info)
        return self._deferred(filename)

    def _handle_series(self, filename, file_info):
        """
        Add or update an episode to the store.
        """
        show = db.query(Show).filter(Show.title.like(file_info.title)).first()
        if not show:
            get_series_metadata(file_info.title).addCallback(
                self._got_series_metadata, filename, file_info)
        else:
            pass

    def _got_series_metadata(self, data, filename, file_info):
        """
        Handles adding or updating the series metadata in the database.
        """

        # If the show doesn't exist it needs to be created
        if not show:
            show = Show()
            db.add(show)

        # Add or update the show metadata
        show.series_id = int(data.id)
        show.title = data.seriesname
        show.description = data.overview
        show.genre = data.genre
        show.rating = data.rating
        show.cover = data.poster
        show.backdrop = data.fanart
        db.commit()

        return get_season_metadata(show.series_id,
            file_info.season).addCallback(self._got_season_metadata,
                show, filename, file_info)

    def _got_season_metadata(self, data, show, filename, file_info):
        """
        Handles adding or updating the season metadata to the database.
        """
        season = db.query(Season).filter_by(show_id=show.id).first()

        # If the season doesn't exist, needs to be created
        if not season:
            season = Season()
            show.seasons.append(season)

        season.number = data.season
        db.commit()
        
        log.info('Fetching metadata for %s S%dE%d', file_info.title,
            file_info.season, file_info.episode)
        return get_episode_metadata(show.series_id, season.number,
            file_info.episode).addCallback(self._got_episode_metadata,
                season, filename, file_info)

    def _got_episode_metadata(self, data, season, filename, file_info):
        """
        Handles adding or updating the episode metadata in the database.
        """
        episode = db.query(Episode).filter_by(
            season  = season,
            episode = file_info.episode).first()

        # Create the Episode is need be
        if not episode:
            log.debug('Adding %s S%dE%d to the database', file_info.title,
                file_info.season, file_info.episode)
            episode = Episode()
            episode.episode = file_info.episode
            season.episodes.append(episode)

        # Set the path just in case the file has been moved
        episode.path = filename

        # Update any metadata that we need to
        if episode.lastupdated < int(data.lastupdated):
            episode.title = data.episodename
            episode.overview = data.overview
            episode.rating = data.rating
            episode.writer = data.writer
            episode.director = data.director
            episode.guest_stars = data.gueststars
            episode.lastupdated = data.lastupdated

        db.commit()
        #self._callback(filename, episode)
        return episode

    def _update_series_file(self, filename, file_info):
        """
        Update an episode in the store.
        """

    def _handle_movie(self, filename, file_info):
        """
        Handle movies
        """

class ImageHandler(FileHandler):
    """
    Handler for jpg/jpeg files.
    """

    def __call__(self, filename):
        if db.query(Photo).filter_by(path=filename).first():
            self._update_file(filename)
        else:
            self._add_file(filename)
        return self._deferred(filename)

    def _add_file(self, filename):
        """
        Add a photo to the store.
        """
        photo = Photo()
        photo.path = unicode(filename)

        db.add(photo)
        db.commit()
        return photo

    def _update_file(self, filename):
        """
        Update an existing image in the store.
        """
        # TODO: There's no metadata currently, so just return the existing
        # object.
        return db.query(Photo).filter_by(path=filename).one()

class MusicHandler(FileHandler):
    """
    Handler for music files.
    """

    def __call__(self, filename):
        return self._deferred(filename)
