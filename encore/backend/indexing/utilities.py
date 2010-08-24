#
# encore/backend/indexing/utilities.py
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

import gst
import logging
import datetime

log = logging.getLogger(__name__)

class TagGetter(object):
    """
    A utility class for getting metadata from mp3 files.
    """

    def __init__(self, filename):
        self.tags = {}

        self.pipeline = gst.parse_launch(
            'filesrc location=%s ! id3demux ! fakesink' % filename)

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message::tag', self.handle_bus_message_tag)
        self.pipeline.set_state(gst.STATE_PAUSED)

        while True:
            message = bus.pop()
            if not message:
                continue
            if message.type == gst.MESSAGE_TAG:
                for key in message.parse_tag().keys():
                    self.tags[key] = message.parse_tag()[key]
                break

    def handle_bus_message_tag(self, message):
        """
        Handle the 'message::tag' bus message.
        """
        taglist = message.parse_tag()
        for key in taglist.keys():
            self.tags[key] = taglist[key]

    def __getattr__(self, attr):
        # TODO: handle types better

        val = self.tags.get(attr.replace('_', '-'))

        if val is None:
            return None

        if type(val) == gst.Date:
            return datetime.date(val.year, val.month, val.day)

        try:
            return int(val)
        except ValueError:
            pass

        if type(val) == str:
            return unicode(val)

        return val
