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

from encore.config import config
from encore.backend.model import *
from encore.backend.indexing.utilities import TagGetter
from encore.backend.indexing.video_metadata import *

class FileHandler(object):
    """
    Abstract class for all indexing file handlers.
    """

    def __call__(self, filename):
        raise NotImplementedError

class VideoHandler(FileHandler):
    """
    Base-class for indexing video files.
    """

    def __call__(self, filename):
        file_info = parse_path(filename)
        if file_info.season:
            self._handle_series(filename, file_info)
        else:
            self._handle_movie(filename, file_info)

    def _handle_series(self, filename, file_info):
        if db.query(Episode).filter_by(path=filename).first():
            return self._update_series_file(filename, file_info)
        else:
            return self._add_series_file(filename, file_info)

    def _add_series_file(self, filename, file_info):
        """
        Add a new episode to the store.
        """

    def _update_series_file(self, filename, file_info):
        """
        Update an episode in the store.
        """

class ImageHandler(FileHandler):
    """
    Handler for jpg/jpeg files.
    """

    def __call__(self, filename):
        if db.query(Photo).filter_by(path=filename).first():
            return self._update_file(filename)
        else:
            return self._add_file(filename)

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
        pass
