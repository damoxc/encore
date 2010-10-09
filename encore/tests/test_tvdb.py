#
# encore/tests/test_tvdb.py
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
import subprocess

from encore.backend.indexing.video_metadata import TVDB_KEY
from encore.lib.tvdb import TvDb, Series, Season, Episode

from encore.tests.test import EncoreTest

class TestTvDb(EncoreTest):
    """
    Tests the twisted based tvdb-api
    """

    def setUp(self):
        super(TestTvDb, self).setUp()
        self.tvdb = TvDb(TVDB_KEY)

    def test_constructor(self):
        self.assertTrue(isinstance(self.tvdb, TvDb))

    def test_get_languages(self):

        def got_languages(languages):
            self.assertTrue(isinstance(languages, list))
            self.assertTrue(len(languages) > 0)

        return self.tvdb.get_languages().addCallback(got_languages)

    def test_get_series(self):

        def got_series(series):
            self.assertTrue(isinstance(series, Series))
            self.assertEqual(series.id, '82283')

        return self.tvdb.get_series('true blood').addCallback(got_series)

    def test_get_season(self):

        def got_series(series):
            season = series[1]
            self.assertTrue(isinstance(season, Season))

        return self.tvdb.get_series_by_id(82283).addCallback(got_series)

    def test_get_season_banners(self):

        def got_banners(banners, season):
            self.assertTrue(isinstance(banners, list))

        def got_series(series):
            season = series[1]
            return season.get_banners().addCallback(got_banners, season)

        return self.tvdb.get_series_by_id(82283).addCallback(got_series)

    def test_download_banner(self):

        def downloaded_banner(response, path):
            self.assertTrue(os.path.isfile(path))
            p = subprocess.Popen(['sha1sum', path], stdout=subprocess.PIPE)
            sha1sum = p.stdout.read().strip().split()[0]
            self.assertEqual(sha1sum,
                '0e0d1ce723c972097a36a20c68e76ab684d8f45e')

        def got_banners(banners):
            for banner in banners:
                if banner.bannertype != 'poster':
                    continue
                break
            
            path = 'banner-%s.jpg' % banner.id

            return banner.download(path).addCallback(downloaded_banner,
                path)

        return self.tvdb.get_banners(82283).addCallback(got_banners)

    def test_get_banners(self):

        def got_banners(banners):
            self.assertTrue(isinstance(banners, list))
            self.assertTrue(len(banners) > 0)

        return self.tvdb.get_banners(82283).addCallback(got_banners)

    def test_get_episode(self):

        def got_episode(episode):
            self.assertTrue(isinstance(episode, Episode))
            self.assertEqual(episode.id, '532631')

        return self.tvdb.get_episode(82283, 2, 3).addCallback(got_episode)
