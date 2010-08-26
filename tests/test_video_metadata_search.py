#
# tests/test_video_video_info.py
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

from encore.backend.indexing.video_metadata_search import *

from tests import EncoreTest

class TestVideoMetadataParsePath(EncoreTest):
    """
    Tests encore.backend.indexing.video_video_info.parse_path
    """

    def test_return_type(self):
        """
        Ensure that the parse_path function returns a VideoFileInfo
        namedtuple.
        """
        filename = '/home/user/videos/Futurama s02e05 something.avi'
        video_info = parse_path(filename)
        self.assertTrue(isinstance(video_info, VideoFileInfo))

    def test_series_title(self):
        """
        Ensure that a series title is returned correctly.
        """
        filename = '/home/user/videos/Futurama s02e05 something.avi'
        video_info = parse_path(filename)
        self.assertEqual(video_info.title, 'futurama')

    def test_series_title_dir(self):
        """
        Ensures that a series title is returned correctly when the 
        show and season are specified by parent directories.
        """
        filename = '/home/user/videos/Futurama/Season 2/05 something.avi'
        video_info = parse_path(filename)
        self.assertEqual(video_info.title, 'futurama')

        filename = '/home/user/videos/Futurama - Season 2/05 something.avi'
        video_info = parse_path(filename)
        self.assertEqual(video_info.title, 'futurama')

    def test_series_season(self):
        """
        Ensure a series season is returned correctly.
        """
        filename = '/home/user/videos/Futurama s02e05 something.avi'
        video_info = parse_path(filename)
        self.assertEqual(video_info.season, 2)

    def test_series_season_dir(self):
        """
        Ensure that a series season is returned correctly when gathered
        from a parent directory.
        """
        filename = '/home/user/videos/Futurama/Season 2/05 something.avi'
        video_info = parse_path(filename)
        self.assertEqual(video_info.season, 2)

        filename = '/home/user/videos/Futurama - Season 2/05 something.avi'
        video_info = parse_path(filename)
        self.assertEqual(video_info.season, 2)

    def test_series_episode(self):
        """
        Ensure a series episode is returned correctly.
        """
        filename = '/home/user/videos/Futurama s02e05 something.avi'
        video_info = parse_path(filename)
        self.assertEqual(video_info.episode, 5)

    def test_series_episode_dir(self):
        """
        Ensure a series episode is returned correctly when using parent
        directories.
        """
        filename = '/home/user/videos/Futurama/Season 2/05 something.avi'
        video_info = parse_path(filename)
        self.assertEqual(video_info.episode, 5)

        filename = '/home/user/videos/Futurama - Season 2/05 something.avi'
        video_info = parse_path(filename)
        self.assertEqual(video_info.episode, 5)
