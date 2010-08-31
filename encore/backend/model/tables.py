#
# encore/model/tables.py
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

from sqlalchemy import MetaData, Table, Column, ForeignKey
from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text, Time

meta = MetaData()

movies = Table('movies', meta,
    Column('id', Integer, primary_key=True),
    Column('movie_id', String(10)),
    Column('path', String(200)),
    Column('description', Text),
    Column('genre', String(100)),
    Column('rating', Float),
    Column('cover', String(100)),
    Column('backdrop', String(100))
)

photos = Table('photos', meta,
    Column('id', Integer, primary_key=True),
    Column('path', String(200))
)

shows = Table('shows', meta,
    Column('id', Integer, primary_key=True),
    Column('series_id', String(10)),
    Column('title', String(100)),
    Column('description', Text),
    Column('genre', String(100)),
    Column('rating', Float),
    Column('cover', String(100)),
    Column('backdrop', String(100))
)

seasons = Table('seasons', meta,
    Column('id', Integer, primary_key=True),
    Column('show_id', Integer, ForeignKey('shows.id'),
    Column('season', Integer),
    Column('banner', String(100))
)

episodes = Table('episodes', meta,
    Column('id', Integer, primary_key=True),
    Column('show_id', Integer, ForeignKey('shows.id')),
    Column('path', String(200)),
    Column('season', Integer),
    Column('episode', Integer),
    Column('title', String(100)),
    Column('image', String(100))
)
