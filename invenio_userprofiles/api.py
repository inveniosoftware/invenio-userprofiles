# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2022 CERN.
# Copyright (C) 2021      TU Wien.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""API for user profiles."""

from warnings import warn

from flask_security import current_user
from werkzeug.local import LocalProxy

from .models import UserProfileProxy


def _get_current_userprofile():
    """Get current user profile.

    .. note:: If the user is anonymous, then a
        :class:`invenio_userprofiles.models.AnonymousUserProfile` instance is
        returned.

    :returns: The :class:`invenio_userprofiles.models.UserProfile` instance.
    """
    warn(
        "current_userprofile is deprecated, use current_user instead",
        DeprecationWarning,
    )
    return UserProfileProxy(current_user)


current_userprofile = LocalProxy(lambda: _get_current_userprofile())
"""Proxy to the user profile of the currently logged in user."""
