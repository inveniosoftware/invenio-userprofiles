# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016, 2017 CERN.
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

"""Minimal Flask application example for development.

SPHINX-START

First install Invenio-UserProfiles, setup the application and load fixture data
by running:

.. code-block:: console

   $ pip install -e .[all]
   $ cd examples
   $ ./app-setup.sh
   $ ./app-fixtures.sh

You should also have the `Redis` running on your machine. To know how
to install and run `redis`, please refer to the
`redis website <https://redis.io/>`_.

Next, start the development server:

.. code-block:: console

   $ export FLASK_APP=app.py FLASK_DEBUG=1
   $ flask run

and open the example application in your browser:

.. code-block:: console

    $ open http://127.0.0.1:5000/

Choose a user to login:

    - user info@inveniosoftware.org password 123456
    - user another@inveniosoftware.org password 123456

You can check the administration page opening the page:

    $ open http://127.0.0.1:5000/admin

Note that, as defined in our fixtures, only `info@inveniosoftware.org` user
can enter.

To uninstall and purge the example app, run:

.. code-block:: console

    $ ./app-teardown.sh

SPHINX-END
"""

from __future__ import absolute_import, print_function

import os

import pkg_resources
from flask import Flask, flash, redirect, request, url_for
from flask_babelex import lazy_gettext as _
from flask_babelex import Babel
from flask_login import current_user
from invenio_access import InvenioAccess
from invenio_accounts import InvenioAccounts
from invenio_accounts.models import User
from invenio_accounts.views import blueprint
from invenio_admin import InvenioAdmin
from invenio_admin.views import blueprint as blueprint_admin_ui
from invenio_db import InvenioDB, db
from invenio_i18n import InvenioI18N
from invenio_mail import InvenioMail
from sqlalchemy import event
from wtforms import StringField, TextAreaField
from wtforms.i18n import messages_path

from invenio_userprofiles import InvenioUserProfiles
from invenio_userprofiles.api import current_userprofile
from invenio_userprofiles.forms import EmailProfileForm
from invenio_userprofiles.views import blueprint as blueprint2
from invenio_userprofiles.views import blueprint_api_init, blueprint_ui_init

try:
    pkg_resources.get_distribution('invenio_assets')
    from invenio_assets import InvenioAssets
    INVENIO_ASSETS_AVAILABLE = True
except pkg_resources.DistributionNotFound:
    INVENIO_ASSETS_AVAILABLE = False

try:
    pkg_resources.get_distribution('invenio_theme')
    from invenio_theme import InvenioTheme
    INVENIO_THEME_AVAILABLE = True
except pkg_resources.DistributionNotFound:
    INVENIO_THEME_AVAILABLE = False


class DetailedProfile(db.Model):
    """DetailedProfile model."""

    __tablename__ = 'userprofiles_example_detailed_profile'
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    detailed_profile = db.relationship(
        User, backref=db.backref(
            'detailed_profile', uselist=False, cascade='all, delete-orphan'))
    bio = db.Column(db.Text)
    affiliation = db.Column(db.String(255))

    @classmethod
    def get_by_userid(cls, user_id):
        """Get profile by user identifier."""
        return cls.query.filter_by(user_id=user_id).one_or_none()


@event.listens_for(User, 'init')
def on_user_init(target, args, kwargs):
    """Provide hook on User initialization."""
    detailed_profile = DetailedProfile()
    if kwargs.get('id'):
        detailed_profile.user_id = kwargs['id']
    kwargs['detailed_profile'] = detailed_profile


class EmailDetailedProfileForm(EmailProfileForm):
    """Form for Extending EmailProfile class."""

    bio = TextAreaField(_('Short Bio'), description=_('Optional'))
    affiliation = StringField(_('Affiliation'), description=_('Optional'))


# Create Flask application
app = Flask(__name__)
app.config.update(
    ACCOUNTS_USE_CELERY=False,
    BABEL_DEFAULT_LOCALE='en',
    I18N_TRASNLATION_PATHS=[messages_path()],
    MAIL_SUPPRESS_SEND=True,
    SECRET_KEY='CHANGE_ME',
    SQLALCHEMY_DATABASE_URI=os.environ.get(
        'SQLALCHEMY_DATABASE_URI', 'sqlite:///test.db'
    ),
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    WTF_CSRF_ENABLED=False,
    USERPROFILES_EMAIL_ENABLED=True,
)
Babel(app)
InvenioMail(app)
InvenioI18N(app)
InvenioDB(app)
if INVENIO_ASSETS_AVAILABLE:
    InvenioAssets(app)
if INVENIO_THEME_AVAILABLE:
    InvenioTheme(app)
InvenioAccess(app)
InvenioAccounts(app)
app.register_blueprint(blueprint)
InvenioUserProfiles(app)
app.register_blueprint(blueprint2)
app.register_blueprint(blueprint_api_init)
app.register_blueprint(blueprint_ui_init)

InvenioAdmin(app)
app.register_blueprint(blueprint_admin_ui)


def detailed_profile_form_factory():
    """Create a profile page form."""
    return EmailDetailedProfileForm(
        formdata=None,
        username=current_userprofile.username,
        full_name=current_userprofile.full_name,
        email=current_user.email,
        email_repeat=current_user.email,
        bio=current_user.detailed_profile.bio,
        affiliation=current_user.detailed_profile.affiliation,
        prefix='profile'
    )


def handle_profile_form(form):
    """Handle profile update form."""
    form.process(formdata=request.form)

    if form.validate_on_submit():
        with db.session.begin_nested():
            current_userprofile.username = form.username.data
            current_userprofile.full_name = form.full_name.data
            db.session.add(current_userprofile)

            detailed_profile = DetailedProfile.get_by_userid(
                current_user.detailed_profile.user_id)
            detailed_profile.bio = form.bio.data
            detailed_profile.affiliation = form.affiliation.data
            db.session.add(detailed_profile)

            if form.email.data != current_user.email:
                current_user.email = form.email.data
                current_user.confirmed_at = None
                db.session.add(current_user)
        db.session.commit()

        flash(_('Profile was updated.'), category='success')

app.config['USERPROFILES_PROFILE_FORM_FACTORY'] = detailed_profile_form_factory
app.config['USERPROFILES_HANDLE_PROFILE_FORM'] = handle_profile_form


@app.route('/')
def index():
    """Example index page route."""
    return redirect(url_for('invenio_userprofiles.profile'))
