#
# encore/model/classes.py
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

from sqlalchemy import and_, join, desc, text
from sqlalchemy.orm import mapper, backref, relation

from encore.backend.model.tables import *

class Movie(object):
    pass

class Photo(object):
    pass

class Show(object):
    pass

class Season(object):
    pass

class Episode(object):
    pass

mapper(Movie, movies)
mapper(Photo, photos)
mapper(Show, shows)
mapper(Season, seasons, properties = {
    'show': relation(Show, uselist=False, backref='seasons')
})
mapper(Episode, episodes, properties = {
    'season': relation(Season, uselist=False, backref='episodes')
})
