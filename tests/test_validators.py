# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Tests for user profile validators."""

from __future__ import absolute_import, print_function

import pytest

from invenio_userprofiles.validators import validate_username

test_usernames = {
    'valid': 'Good-Name_9',
    'invalid_begins_with_number': '9CantStartWithNumber',
    'invalid_characters': '_Containsi!!ega!Char acters*',
    'invalid_short': 'ab',
}


def test_validate_username(app):
    """Test username validator."""
    # Goodname can contain letters, numbers and starts with a letter
    validate_username(test_usernames['valid'])

    # Can't start with a number
    with pytest.raises(ValueError):
        validate_username(test_usernames['invalid_begins_with_number'])

    # Can only contain latin letters and numbers
    with pytest.raises(ValueError):
        validate_username(test_usernames['invalid_characters'])

    with pytest.raises(ValueError):
        validate_username(test_usernames['invalid_short'])
