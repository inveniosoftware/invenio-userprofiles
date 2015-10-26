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

"""Tests for user profile models."""

from __future__ import absolute_import, print_function

import pytest

from test_validators import test_usernames

from invenio_userprofiles import UserProfile


def test_userprofiles(app):
    """Test UserProfile model."""
    profile = UserProfile()

    # Check the username validator works on the model
    profile.username = test_usernames['valid']
    with pytest.raises(ValueError):
        profile.username = test_usernames['invalid_characters']
    with pytest.raises(ValueError):
        profile.username = test_usernames['invalid_begins_with_number']

    # Test non-validated attributes
    profile.first_name = 'Test'
    profile.last_name = 'User'
    assert profile.first_name == 'Test'
    assert profile.last_name == 'User'
