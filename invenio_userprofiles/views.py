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

"""Invenio module that adds userprofiles to the platform."""

from __future__ import absolute_import, print_function

from flask import Blueprint, render_template, request
from flask_babelex import gettext as _
from flask_menu import current_menu
from flask_security import login_required

from invenio_db import db

from .api import current_userprofile
from .forms import ProfileForm

blueprint = Blueprint(
    'invenio_userprofiles',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@blueprint.before_app_first_request
def init_menu():
    """Initialize menu before first request."""
    item = current_menu.submenu('settings.userprofiles')
    item.register(None, _('User Profile'))

    item = current_menu.submenu('settings.userprofiles.profile')
    item.register(
        'invenio_userprofiles.profile',
        _('%(icon)s Profile', icon='<i class="fa fa-user fa-fw"></i>'))


@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """View for editing profile."""
    form = ProfileForm(obj=current_userprofile)

    if request.method == 'POST' and form.validate():
        with db.session.begin_nested():
            current_userprofile.username = form.username.data
            current_userprofile.full_name = form.full_name.data

    return render_template("invenio_userprofiles/settings/profile.html",
                           form=form)
