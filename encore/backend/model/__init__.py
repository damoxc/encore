#
# encore/model/__init__.py
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

from sqlalchemy import create_engine, func, text
from sqlalchemy.orm import sessionmaker, scoped_session

from encore.backend.model.classes import *
from encore.component import Component
from encore.config import config

class Database(Component):

    def __init__(self):
        super(Database, self).__init__('Database')
        self.engine = None
        
    def initialize(self):
        dburi = 'sqlite:///' + config.DB_FILE
        self.engine = create_engine(dburi)
        sm = sessionmaker(autoflush=False, autocommit=False,
            bind=self.engine)
        self.Session = scoped_session(sm)

        # Create the database if it doesn't already exist
        if not os.path.isfile(config.DB_FILE):
            meta.create_all(bind=self.engine)

    def add(self, *args):
        return self.Session.add(*args)

    def commit(self):
        return self.Session.commit()

    def query(self, *args, **kwargs):
        return self.Session.query(*args, **kwargs)

    def session(self):
        return self.Session()

db = Database()
