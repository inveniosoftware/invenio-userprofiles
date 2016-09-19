# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016 CERN.
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

"""User profiles module for Invenio."""

from __future__ import absolute_import, print_function

from . import config
import pkg_resources
from invenio_db import db
from sqlalchemy.exc import InvalidRequestError

from invenio_admin.views import protected_adminview_factory
from .api import current_userprofile


class _UserProfileState(object):
    """State for Invenio-Admin."""

    def __init__(self, app):
        """Initialize state."""
        # Create admin instance.
        self.app = app
        self.model = None
        self.admin_view = None

    def load_model_entry_point_group(self, entry_point_group):
        """Load administration interface from entry point group."""

        for ep in pkg_resources.iter_entry_points(group=entry_point_group):
            try:

                if self.model is None:
                    self.model = ep.load()

            except InvalidRequestError:
                print("Unable to load AUTH_USER_MODEL")

    def load_admin_entry_point_group(self, entry_point_group):
        """Load administration interface from entry point group."""

        print("LOADING ADMIN ENTRY POINT")
        print(self.app.extensions['invenio-admin'])

        for ep in pkg_resources.iter_entry_points(group=entry_point_group):
            try:

                if self.admin_view is None:
                    self.admin_view = ep.load()

                    view_class = protected_adminview_factory(self.admin_view)
                    print("Hi!")
                    print(view_class)
                    self.app.extensions['invenio-admin'].add_view(
                        view_class(self.model, db.session))

            except Exception as e:
                print("Unable to load AUTH_ADMIN vire")
                print(e)


class InvenioUserProfiles(object):
    """Invenio-UserProfiles extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app, model_entry_point_group='invenio_userprofiles.auth_models',
                 admin_entry_point_group='invenio_userprofiles.auth_admin'):
        """Flask application initialization."""
        self.init_config(app)

        # Register current_profile
        app.context_processor(lambda: dict(
            current_userprofile=current_userprofile))

        # Create user profile state
        state = _UserProfileState(app)

        if model_entry_point_group:
            state.load_model_entry_point_group(model_entry_point_group)

        # if admin_entry_point_group:
        #     state.load_admin_entry_point_group(admin_entry_point_group)

        app.extensions['invenio-userprofile'] = state
        return state

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith('USERPROFILES_'):
                app.config.setdefault(k, getattr(config, k))

        app.config.setdefault('USERPROFILES', True)

        app.config.setdefault(
            'USERPROFILES_BASE_TEMPLATE',
            app.config.get('BASE_TEMPLATE',
                           'invenio_userprofiles/base.html'))

        app.config.setdefault(
            'USERPROFILES_SETTINGS_TEMPLATE',
            app.config.get('SETTINGS_TEMPLATE',
                           'invenio_userprofiles/settings/base.html'))

        if app.config['USERPROFILES_EXTEND_SECURITY_FORMS']:
            app.config.setdefault(
                'USERPROFILES_REGISTER_USER_BASE_TEMPLATE',
                app.config.get(
                    'SECURITY_REGISTER_USER_TEMPLATE',
                    'invenio_accounts/register_user.html'
                )
            )
            app.config['SECURITY_REGISTER_USER_TEMPLATE'] = \
                'invenio_userprofiles/register_user.html'
