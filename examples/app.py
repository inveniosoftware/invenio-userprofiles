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


u"""Minimal Flask application example for development.

Install the Invenio default theme

You should execute these commands in the examples-directory.

.. code-block:: console
   $ pip install -r requirements.txt
   $ flask -a app.py bower
   $ cd instance
   $ bower install
   $ cd ..
   $ flask -a app.py collect -v
   $ flask -a app.py assets build

Create database and tables:

.. code-block:: console

   $ flask -a app.py db init
   $ flask -a app.py db create

Run the development server:

.. code-block:: console

   $ flask -a app.py --debug run
"""

from __future__ import absolute_import, print_function

import pkg_resources

from flask import Flask, redirect, url_for
from flask_babelex import Babel
from flask_cli import FlaskCLI
from flask_mail import Mail

from invenio_accounts import InvenioAccounts
from invenio_accounts.views import blueprint
from invenio_db import InvenioDB
from invenio_userprofiles import InvenioUserProfiles

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
    MAIL_SUPPRESS_SEND=True,
    SECRET_KEY='CHANGE_ME',
    ACCOUNTS_USE_CELERY=False,
)
FlaskCLI(app)
Babel(app)
Mail(app)
InvenioDB(app)
if INVENIO_ASSETS_AVAILABLE:
    InvenioAssets(app)
if INVENIO_THEME_AVAILABLE:
    InvenioTheme(app)
InvenioAccounts(app)
app.register_blueprint(blueprint)
InvenioUserProfiles(app)


@app.route('/')
def index():
    """Example index page route."""
    return redirect(url_for('invenio_userprofiles.profile'))
