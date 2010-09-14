#
# encore/config.py
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
import subprocess

from xdg import BaseDirectory

from encore.component import Component
from encore.utils.oproxy import ObjectProxy

class Config(Component):

    def __init__(self):
        super(Config, self).__init__('Config')
        self.test_dir = None
        self._config = {}

    def initialize(self):
        if self.test_dir is None:
            self.resources = Resources()
        else:
            self.resources = Resources(config_testing_dir=self.test_dir)

        self.cache_dir = self.resources.cache_dir
        self.config_dir = self.resources.config_dir
        self.data_dir = self.resources.data_dir

        self.LOG_FILE = os.path.join(self.cache_dir, 'encore.log')
        self.DB_FILE = os.path.join(self.cache_dir, 'media.db')

        self.THUMB_DIR = os.path.join(self.cache_dir, 'thumbnails')
        self.IMAGE_THUMB_DIR = os.path.join(self.THUMB_DIR, 'image')
        self.VIDEO_THUMB_DIR = os.path.join(self.THUMB_DIR, 'video')
        self.ALBUM_ART_DIR = os.path.join(self.cache_dir, 'album_art')
        self.MOVIE_ART_DIR = os.path.join(self.cache_dir, 'movie_art')

        self.read_config_file()

        self.network_options = {
            'type': 'local',
            'host': 'localhost',
            'port': 55545
        }

    def get_video_directories(self):
        """
        Returns all the directories configured to scan for video content.

        :returns: list of the directories
        :rtype: list
        """

        if 'video_dirs' in self._config:
            return self._config['video_dirs']

        # TODO: Move this code into a common function to make it easier
        # to load up other directories.

        # Check for the ~/.config/user-dirs.dirs file
        user_dirs = BaseDirectory.load_first_config('user-dirs.dirs')
        if not user_dirs:
            # Attempt to generate out the default user-dirs.dirs config
            try:
                subprocess.call(['xdg-user-dirs-update'])
            except OSError:
                return []

        # If the file still doesn't exist then something is very wrong
        # so just fail with an empty list.
        if not BaseDirectory.load_first_config('user-dirs.dirs'):
            return []

        # Load the user-dirs.dirs config file to get the configured videos
        # directory.
        for line in open(BaseDirectory.load_first_config('user-dirs.dirs')):
            line = line.strip()
            if line.startswith('#'):
                continue
            (name, value) = line.split('=', 1)
            if name == 'XDG_VIDEOS_DIR':
                return [os.path.expandvars(value[1:-1])]

        return []

    def read_config_file(self):
        pass

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


config = Config()
