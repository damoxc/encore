#
# encore/misc/oproxy.py
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

class ObjectProxy(object):

    def __init__(self):
        self._wrapped = None

    def _set_wrapped(self, wrapped):
        object.__setattr__(self, '_wrapped', wrapped)

    def __getattr__(self, key):
        if hasattr(self._wrapped, key):
            return getattr(self._wrapped, key)
        raise AttributeError()
