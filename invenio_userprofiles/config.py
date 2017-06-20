# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
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

"""Default configuration."""

USERPROFILES = True
"""Enable or disable module extensions."""

USERPROFILES_EMAIL_ENABLED = True
"""Include the user email in the profile form."""

USERPROFILES_EXTEND_SECURITY_FORMS = False
"""Extend the Invenio-Accounts user registration forms."""

USERPROFILES_PROFILE_TEMPLATE = 'invenio_userprofiles/settings/profile.html'
"""Default profile template."""

USERPROFILES_PROFILE_URL = '/account/settings/profile/'
"""Default profile URL endpoint."""

USERPROFILES_BASE_TEMPLATE = None
"""Base templates for user profile module."""

USERPROFILES_SETTINGS_TEMPLATE = None
"""Settings base templates for user profile module."""
