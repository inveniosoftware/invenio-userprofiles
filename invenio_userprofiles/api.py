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

"""API for user profiles."""

from flask_security import current_user

from invenio_db import db

from werkzeug.local import LocalProxy

from .models import AnonymousUserProfile, UserProfile


def _get_current_userprofile():
    if current_user.is_anonymous():
        return AnonymousUserProfile()

    profile = UserProfile.query.get(current_user.get_id())
    if not profile:
        with db.session.begin_nested():
            profile = UserProfile()
            profile.user_id = current_user.get_id()
            db.session.add(profile)

    return profile


current_userprofile = LocalProxy(lambda: _get_current_userprofile())
