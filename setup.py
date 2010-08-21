#
# setup.py
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

try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages

# Main setup
setup(
    name         = 'encore',
    version      = '0.0.1',
    fullname     = 'Encore Media Centre',
    description  = 'Gnome media centre',
    author       = 'Damien Churchill',
    author_email = 'damoxc@gmail.com',
    keywords     = 'media centre video player',
    long_description = """Encore is a media centre designed to integrate
    into the GNOME desktop""",
    url          = 'encore-project.org',
    license      = 'GPLv3',

    packages = find_packages(exclude=['plugins', 'docs', 'tests']),
    entry_points = """
    [console_scripts]
    encore         = encore.client.main:main
    encore-backend = encore.backend.main:main
    """
)
