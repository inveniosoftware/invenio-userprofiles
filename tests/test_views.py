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

"""Tests for user profile views."""

from __future__ import absolute_import, print_function

from flask import url_for

from helpers import login, sign_up

from test_validators import test_usernames


def test_profile_view_not_accessible_without_login(app):
    """Test the user can't access profile settings page without logging in."""
    with app.app_context():
        with app.test_client() as client:
            resp = client.get(
                url_for('invenio_userprofiles.profile'), follow_redirects=True)
            assert resp.status_code == 200
            assert 'name="login_user_form"' in str(resp.data)


def test_profile_view(app):
    """Test the profile view."""
    with app.app_context():
        with app.test_client() as client:
            sign_up(app, client)
            login(app, client)
            resp = client.get(url_for('invenio_userprofiles.profile'))
            assert resp.status_code == 200
            assert 'name="profile_form"' in str(resp.data)

            # Valid submission should work
            resp = client.post(url_for('invenio_userprofiles.profile'),
                               data=dict(
                username=test_usernames['valid'],
                full_name='Valid Name')
            )
            assert resp.status_code == 200
            assert test_usernames['valid'] in resp.data
            assert 'Valid' in resp.data
            assert 'Name' in resp.data

            # Invalid submission should not save data
            resp = client.post(url_for('invenio_userprofiles.profile'),
                               data=dict(
                username=test_usernames['invalid_characters'],
                full_name='Valid Name'))
            assert resp.status_code == 200
            assert test_usernames['invalid_characters'] in resp.data
            resp = client.get('/profile')
            assert resp.status_code == 200
            assert test_usernames['valid'] in resp.data

            # Whitespace should be trimmed
            client.post(url_for('invenio_userprofiles.profile'), data=dict(
                username='{0} '.format(test_usernames['valid']),
                full_name='Valid Name '))
            resp = client.get(url_for('invenio_userprofiles.profile'))
            assert resp.status_code == 200
            assert test_usernames['valid'] in resp.data
            assert 'Valid Name ' not in resp.data
