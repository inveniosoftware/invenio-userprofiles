# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

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

USERPROFILES_READ_ONLY = False
"""Make the user profiles read-only."""
