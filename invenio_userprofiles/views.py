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

import pkg_resources
from flask import Blueprint, current_app, flash, render_template, request
from flask_babelex import gettext as _
from flask_login import current_user, login_required
from flask_security.confirmable import send_confirmation_instructions
from invenio_db import db

from .api import current_userprofile
from .forms import EmailProfileForm, ProfileForm, VerificationForm

blueprint = Blueprint(
    'invenio_userprofiles',
    __name__,
    template_folder='templates',
)


@blueprint.before_app_first_request
def init_menu():
    """Initialize menu before first request."""
    try:
        pkg_resources.get_distribution('flask-menu')
        from flask_menu import current_menu
        item = current_menu.submenu('settings.userprofiles')
        item.register(None, _('User Profile'))

        item = current_menu.submenu('settings.userprofiles.profile')
        item.register(
            'invenio_userprofiles.profile',
            # NOTE: Menu item text (icon replaced by a user icon).
            _('%(icon)s Profile', icon='<i class="fa fa-user fa-fw"></i>'))
    except pkg_resources.DistributionNotFound:  # pragma: no cover
        # nothing to do.
        pass


@blueprint.route('', methods=['GET', 'POST'])
@login_required
def profile():
    """View for editing profile."""
    # Create forms
    verification_form = VerificationForm(formdata=None, prefix="verification")
    profile_form = profile_form_factory()

    # Process forms
    form = request.form.get('submit', None)
    if form == 'profile':
        handle_profile_form(profile_form)
    elif form == 'verification':
        handle_verification_form(verification_form)

    return render_template(
        current_app.config['USERPROFILES_PROFILE_TEMPLATE'],
        profile_form=profile_form,
        verification_form=verification_form,)


def profile_form_factory():
    """Create a profile form."""
    if current_app.config['USERPROFILES_EMAIL_ENABLED']:
        return EmailProfileForm(
            formdata=None,
            username=current_userprofile.username,
            full_name=current_userprofile.full_name,
            email=current_user.email,
            email_repeat=current_user.email,
            prefix='profile', )
    else:
        return ProfileForm(
            formdata=None,
            obj=current_userprofile,
            prefix='profile', )


def handle_verification_form(form):
    """Handle email sending verification form."""
    form.process(formdata=request.form)

    if form.validate_on_submit():
        send_confirmation_instructions(current_user)
        # NOTE: Flash message.
        flash(_("Verification email sent."), category="success")


def handle_profile_form(form):
    """Handle profile update form."""
    form.process(formdata=request.form)

    if form.validate_on_submit():
        email_changed = False
        with db.session.begin_nested():
            # Update profile.
            current_userprofile.username = form.username.data
            current_userprofile.full_name = form.full_name.data
            db.session.add(current_userprofile)

            # Update email
            if current_app.config['USERPROFILES_EMAIL_ENABLED'] and \
               form.email.data != current_user.email:
                current_user.email = form.email.data
                current_user.confirmed_at = None
                db.session.add(current_user)
                email_changed = True
        db.session.commit()

        if email_changed:
            send_confirmation_instructions(current_user)
            # NOTE: Flash message after successful update of profile.
            flash(_('Profile was updated. We have sent a verification '
                    'email to %(email)s. Please check it.',
                    email=current_user.email),
                  category='success')
        else:
            # NOTE: Flash message after successful update of profile.
            flash(_('Profile was updated.'), category='success')
