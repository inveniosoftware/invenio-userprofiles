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

"""Validators for user profiles."""

from __future__ import absolute_import, print_function

import re

from flask_babelex import lazy_gettext as _

username_regex = re.compile('^[a-zA-Z][a-zA-Z0-9-_]{2}[a-zA-Z0-9-_]*$')

# NOTE: Used for both form help text and for form validation error.
USERNAME_RULES = _(
    'Username must start with a letter, be at least three characters long and'
    ' only contain alphanumeric characters, dashes and underscores.')


def validate_username(username):
    """Validate the username.

    Usernames can only contain numbers and latin letters. They must
    start with a letter.
    """
    if not username_regex.match(username):
        raise ValueError(USERNAME_RULES)
