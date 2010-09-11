#
# tests/__init__.py
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
import shutil
import tempfile

from twisted.trial import unittest

from encore.config import Config
from encore.backend.model import Database

class EncoreTest(unittest.TestCase):
    """
    Test for use in the Encore test suite.
    """

    def setUp(self):
        """
        Set up the basic file I/O requirements.
        """
        self.test_dir = tempfile.mkdtemp(prefix='encore-tests+')
        self.test_cfg_dir = tempfile.mkdtemp(prefix='encore-tests+')
        self.config = Config(self.test_cfg_dir)
        self.data_dir = os.path.dirname(__file__) + '/data'

    def tearDown(self):
        """
        Remove the temporary files created in the test.
        """
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.test_cfg_dir)

class EncoreDbTest(EncoreTest):
    """
    Test that requires a database
    """

    def setupUp(self):
        EncoreTest.setUp(self)
        self.db = Database(tempfile.mkstemp(prefix='encore-tests+'))
