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

"""Forms for user profiles."""

from __future__ import absolute_import, print_function

from flask_babelex import lazy_gettext as _
from flask_login import current_user
from flask_security.forms import email_required, email_validator, \
    unique_user_email
from flask_wtf import Form
from sqlalchemy.orm.exc import NoResultFound
from wtforms import FormField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, StopValidation, \
    ValidationError

from .api import current_userprofile
from .models import UserProfile
from .validators import USERNAME_RULES, validate_username


def strip_filter(text):
    """Filter for trimming whitespace.

    :param text: The text to strip.
    :returns: The stripped text.
    """
    return text.strip() if text else text


def current_user_email(form, field):
    """Stop validation if email equals current user's email."""
    if current_user.email == field.data:
        raise StopValidation()


class ProfileForm(Form):
    """Form for editing user profile."""

    username = StringField(
        # NOTE: Form field label
        _('Username'),
        # NOTE: Form field help text
        description=_('Required. %(username_rules)s',
                      username_rules=USERNAME_RULES),
        validators=[DataRequired(message=_('Username not provided.'))],
        filters=[strip_filter], )

    full_name = StringField(
        # NOTE: Form label
        _('Full name'),
        filters=[strip_filter], )

    def validate_username(form, field):
        """Wrap username validator for WTForms."""
        try:
            validate_username(field.data)
        except ValueError as e:
            raise ValidationError(e)

        try:
            user_profile = UserProfile.get_by_username(field.data)
            if current_userprofile.is_anonymous or \
                    (current_userprofile.user_id != user_profile.user_id and
                     field.data != current_userprofile.username):
                # NOTE: Form validation error.
                raise ValidationError(_('Username already exists.'))
        except NoResultFound:
            return


class EmailProfileForm(ProfileForm):
    """Form to allow editing of email address."""

    email = StringField(
        # NOTE: Form field label
        _('Email address'),
        filters=[lambda x: x.lower() if x is not None else x, ],
        validators=[
            email_required,
            current_user_email,
            email_validator,
            unique_user_email,
        ],
    )

    email_repeat = StringField(
        # NOTE: Form field label
        _('Re-enter email address'),
        # NOTE: Form field help text
        description=_('Please re-enter your email address.'),
        filters=[lambda x: x.lower() if x else x, ],
        validators=[
            email_required,
            # NOTE: Form validation error.
            EqualTo('email', message=_('Email addresses do not match.'))
        ]
    )


class VerificationForm(Form):
    """Form to render a button to request email confirmation."""

    # NOTE: Form button label
    send_verification_email = SubmitField(_('Resend verification email'))


def register_form_factory(Form):
    """Return extended registration form."""
    class RegisterForm(Form):
        """RegisterForm extended with UserProfile details."""

        profile = FormField(ProfileForm, separator='.')

    return RegisterForm


def confirm_register_form_factory(Form):
    """Return extended confirmation of registration form."""
    class ConfirmRegisterForm(Form):
        """RegisterForm extended with UserProfile details."""

        profile = FormField(ProfileForm, separator='.')

    return ConfirmRegisterForm
