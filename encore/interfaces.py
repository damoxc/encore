#
# encore/interfaces.py
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

class IResourceProvider(object):
    pass

class IVideoProvider(IResourceProvider):
    pass

class IMusicProvider(IMusicProvider):
    pass

class IPhotoProvider(IPhotoProvider):
    pass

class IPlayable(object):
    """
    Interface for all objects that can be played with the MediaPlayer.
    The MediaPlayer only plays objects that implement this interface.
    """

    VIDEO_STREAM = 0
    AUDIO_STREAM = 1

    def get_uri(self):
        """
        Get the URI for the media resource.
        """
        raise NotImplementedError

    def get_type(self):
        """
        Get the type (as defined by the IPlayable constants.
        """
        raise NotImplementedError

    def get_title(self):
        """
        Get the title of the object.
        """
        raise NotImplementedError
