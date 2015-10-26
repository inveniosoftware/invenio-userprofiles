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

"""Forms for user profiles."""

from flask_babelex import gettext as _
from flask_wtf import Form

from wtforms import StringField
from wtforms.validators import ValidationError

from .validators import validate_username


def strip_filter(text):
    """Filter for trimming whitespace."""
    return text.strip() if text else text


class ProfileForm(Form):
    """Form for editing user profile."""

    username = StringField(_('Username'), filters=[strip_filter])
    full_name = StringField(_('Full Name'), filters=[strip_filter])

    def validate_username(form, field):
        """Wrap username validator for WTForms."""
        try:
            validate_username(field.data)
        except ValueError as e:
            raise ValidationError(e)
