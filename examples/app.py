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

"""Minimal Flask application example for development.

Start the Redis server.

Install the Invenio default theme and build assets:

.. code-block:: console

   $ pip install -e .[all]
   $ cd examples
   $ ./app-setup.sh
   $ ./app-fixtures.sh

Run the development server:

.. code-block:: console

   $ FLASK_APP=app.py flask run --debugger -p 5000

To be able to uninstall the example app:

.. code-block:: console

    $ ./app-teardown.sh

"""

from __future__ import absolute_import, print_function

import os

import pkg_resources
from flask import Flask, redirect, url_for
from flask_babelex import Babel
from invenio_accounts import InvenioAccounts
from invenio_accounts.views import blueprint
from invenio_admin import InvenioAdmin
from invenio_db import InvenioDB
from invenio_i18n import InvenioI18N
from invenio_mail import InvenioMail
from wtforms.i18n import messages_path

from invenio_userprofiles import InvenioUserProfiles
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


# Create Flask application
app = Flask(__name__)
app.config.update(
    ACCOUNTS_USE_CELERY=False,
    BABEL_DEFAULT_LOCALE='da',
    I18N_TRASNLATION_PATHS=[messages_path()],
    MAIL_SUPPRESS_SEND=True,
    SECRET_KEY='CHANGE_ME',
    SQLALCHEMY_DATABASE_URI=os.environ.get(
        'SQLALCHEMY_DATABASE_URI', 'sqlite:///test.db'
    ),
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    WTF_CSRF_ENABLED=False,
)
Babel(app)
InvenioMail(app)
InvenioI18N(app)
InvenioDB(app)
if INVENIO_ASSETS_AVAILABLE:
    InvenioAssets(app)
if INVENIO_THEME_AVAILABLE:
    InvenioTheme(app)
InvenioAccounts(app)
app.register_blueprint(blueprint)
InvenioUserProfiles(app)
app.register_blueprint(blueprint2)
app.register_blueprint(blueprint_api_init)
app.register_blueprint(blueprint_ui_init)
InvenioAdmin(app, permission_factory=lambda x: x,
             view_class_factory=lambda x: x)


@app.route('/')
def index():
    """Example index page route."""
    return redirect(url_for('invenio_userprofiles.profile'))
