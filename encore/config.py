#
# encore/configuration.py
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
import json
import shutil

from xdg import BaseDirectory

from encore.component import Component

class Config(Component):

    def __init__(self, test_dir=None):
        super(Config, self).__init__('Config')

        if test_dir is None:
            self.resources = Resources()
        else:
            self.resources = Resources(config_testing_dir=test_dir)

class Resources(object):
    """
    A warpper for the XDG directories. Also handles creation of a new setup
    if the Encore directories within the XDG directories are missing.
    """

    def __init__(self, resource='encore', config_testing_dir=None):
        if config_testing_dir is None:
            self.cache_dir = os.path.join(BaseDirectory.xdg_cache_home,
                resource)
            self.config_dir = os.path.join(BaseDirectory.xdg_config_home,
                resource)
            self.data_dir = os.path.join(BaseDirectory.xdg_data_home,
                resource)
        else:
            self.cache_dir = os.path.join(config_testing_dir, 'cache')
            self.config_dir = os.path.join(config_testing_dir, 'config')
            self.data_dir = os.path.join(config_testing_dir, 'data')

        # Ensure that the directories exist.
        if not os.path.exists(self.cache_dir):
            self.create_cache_hierarchy()
        if not os.path.exists(self.config_dir):
            self.create_configuration()
        if not os.path.exists(self.data_dir):
            self.create_initial_data()

    def create_cache_hierarchy(self):
        """
        Create the cache hierarchy that is assumed to exist.
        """
        os.makedirs(os.path.join(self.cache_dir, 'album_art'))
        os.makedirs(os.path.join(self.cache_dir, 'movie_art'))
        os.makedirs(os.path.join(self.cache_dir, 'thumbnails', 'image'))
        os.makedirs(os.path.join(self.cache_dir, 'thumbnails', 'video'))

    def create_configuration(self):
        """
        Create the user's configuration area and populate with the default
        content configuration.
        """

    def create_initial_data(self):
        """
        Create the initial data directory and populate it with the default
        data used by Encore.
        """
        os.mkdir(self.data_dir)
