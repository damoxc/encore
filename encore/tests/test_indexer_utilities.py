#
# encore/tests/test_indexer_utilities.py
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
import datetime

from encore.tests.test import EncoreTest
from encore.backend.indexing.utilities import TagGetter

class TestTagGetter(EncoreTest):
    """
    Tests for encore.backend.indexing.utilities.TagGetter.
    """

    def test_constructor(self):
        tag_getter = TagGetter(os.path.join(self.data_dir, 'test.mp3'))
        self.assertTrue(isinstance(tag_getter, TagGetter))

    def test_missing_file(self):
        self.assertRaises(IOError, TagGetter, 'missing.mp3')

    def test_get_tags(self):
        """
        Test TagGetter.get_tags.
        """
        tag_getter = TagGetter(os.path.join(self.data_dir, 'test.mp3'))
        self.assertEqual(tag_getter.artist, 'Iron and Wine')
        self.assertEqual(tag_getter.album, 'The Shephard\'s Dog')
        self.assertEqual(tag_getter.genre, 'Gangster Rap')
        self.assertEqual(tag_getter.title, 'Flightless Bird, American Mouth')
        self.assertEqual(tag_getter.comment, 'This is a comment')
        self.assertEqual(tag_getter.track_number, 12) 
        self.assertEqual(tag_getter.album_disc_number, 1)
        self.assertEqual(tag_getter.date, datetime.date(2000, 01, 01))

    def test_get_invalid_tags(self):
        """
        Test TagGetter.get_tags with noexistent tags.
        """
        tag_getter = TagGetter(os.path.join(self.data_dir, 'test.mp3'))
        self.assertEqual(tag_getter.some_missing_tag, None)
