#
# encore/backend/indexing/indexer.py
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
import logging

from encore.component import Component
from encore.config import config
from encore.backend.indexing import handlers

log = logging.getLogger(__name__)

class Indexer(Component):
    """
    The main indexer that indexes all the media folders registered in
    Encore.
    """

    handlers = {
        'avi': handlers.VideoHandler(),
        'jpg': handlers.ImageHandler(),
        'jpeg': handlers.ImageHandler(),
        'm4v': handlers.VideoHandler(),
        'mkv': handlers.VideoHandler(),
        'mov': handlers.VideoHandler(),
        'mp3': handlers.MusicHandler(),
        'mp4': handlers.VideoHandler(),
        'mpeg': handlers.VideoHandler(),
        'mpg': handlers.VideoHandler(),
        'ogg': handlers.MusicHandler(),
        'ogm': handlers.VideoHandler(),
        'png': handlers.ImageHandler(),
        'wmv': handlers.VideoHandler()
    }

    def run(self):
        """
        Start the indexer running.
        """
        print config

    @property
    def supported_filetypes(self):
        """
        Return a list of all supported filetypes.
        """
        return self.handlers.keys()

    def get_filetype_handler(self, filetype):
        """
        Return the handler for a given filetype.
        """
        return self.handlers.get(filetype, None)

    def is_supported_filetype(self, filename):
        """
        Check whether or not a file is supported by the indexer.
        """
        extension = filename.split('.')[-1]
        return extension in self.supported_filetypes
