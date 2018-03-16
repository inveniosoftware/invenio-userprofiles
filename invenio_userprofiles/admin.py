# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Admin views for invenio-userprofiles."""

from __future__ import absolute_import, print_function

from flask_admin.contrib.sqla import ModelView

from .models import UserProfile


def _(x):
    """Identity."""
    return x


class UserProfileView(ModelView):
    """Userprofiles view. Links User ID to user/full/display name."""

    can_view_details = True
    can_create = False
    can_delete = False

    column_list = (
        'user_id',
        '_displayname',
        'full_name',
    )

    column_searchable_list = \
        column_filters = \
        column_details_list = \
        columns_sortable_list = \
        column_list

    form_columns = ('username', 'full_name')

    column_labels = {
        '_displayname': _('Username'),
    }


user_profile_adminview = {
    'model': UserProfile,
    'modelview': UserProfileView,
    'category': _('User Management'),
}
