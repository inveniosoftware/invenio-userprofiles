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

"""Database models for user profiles."""

from __future__ import absolute_import, print_function

from invenio_accounts.models import User
from invenio_db import db

from sqlalchemy.orm import validates

from .validators import validate_username


class AnonymousUserProfile():
    """Anonymous user profile."""

    def is_anonymous(self):
        """Return whether this UserProfile is anonymous."""
        return True


class UserProfile(db.Model):
    """UserProfile model.

    UserProfiles store information about account users.
    """

    __tablename__ = 'userprofiles_userprofile'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    username = db.Column(db.String(255), unique=True)

    full_name = db.Column(db.String(255))

    @validates('username')
    def _validate_username(self, key, username):
        """Wrap username validator for SQLAlchemy."""
        validate_username(username)
        return username

    def is_anonymous(self):
        """Return whether this UserProfile is anonymous."""
        return False
