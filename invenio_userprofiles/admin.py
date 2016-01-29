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

"""Admin views for invenio-userprofiles."""

from flask_admin.contrib.sqla import ModelView

from .models import UserProfile


def _(x):
    """Identity."""
    return x


class UserProfileView(ModelView):
    """Userprofiles view. Links User ID to user/full/display name."""

    can_view_details = True
    can_delete = False

    column_list = (
        'user_id',
        'username',
        '_displayname',
        'full_name',
    )

    form_columns = \
        column_searchable_list = \
        column_filters = \
        column_details_list = \
        columns_sortable_list = \
        column_list

    column_labels = {
        "_displayname": _('Display Name'),
    }

user_profile_adminview = {
    'model': UserProfile,
    'modelview': UserProfileView,
    'category': _('User Management'),
}
