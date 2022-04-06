# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""User profiles module for Invenio."""

from .api import current_userprofile
from .ext import InvenioUserProfiles
from .models import AnonymousUserProfile, UserProfile

__version__ = '1.2.4'

__all__ = ('__version__', 'InvenioUserProfiles', 'AnonymousUserProfile',
           'UserProfile', 'current_userprofile')
