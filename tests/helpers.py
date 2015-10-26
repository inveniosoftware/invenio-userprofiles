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


"""Helper functions for tests."""

from __future__ import absolute_import, print_function

from flask import url_for


def sign_up(app, client):
    """Register a user."""
    client.post(url_for('security.register'), data=dict(
        email=app.config['TEST_USER_EMAIL'],
        password=app.config['TEST_USER_PASSWORD'],
    ), environ_base={'REMOTE_ADDR': '127.0.0.1'})


def login(app, client):
    """Log the user in with the test client."""
    client.post(url_for('security.login'), data=dict(
        email=app.config['TEST_USER_EMAIL'],
        password=app.config['TEST_USER_PASSWORD'],
    ))
