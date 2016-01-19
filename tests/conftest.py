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

"""Pytest configuration."""

from __future__ import absolute_import, print_function

import os
import shutil
import tempfile

import pytest
from flask import Flask
from flask_babelex import Babel
from flask_cli import FlaskCLI
from flask_mail import Mail
from flask_menu import Menu
from invenio_accounts import InvenioAccounts
from invenio_accounts.views import blueprint
from invenio_db import InvenioDB, db
from sqlalchemy_utils.functions import create_database, database_exists, \
    drop_database

from invenio_userprofiles import InvenioUserProfiles


@pytest.fixture
def base_app():
    """Flask application fixture."""
    instance_path = tempfile.mkdtemp()
    base_app = Flask(__name__, instance_path=instance_path)

    base_app.config.update(
        ACCOUNTS_USE_CELERY=False,
        LOGIN_DISABLED=False,
        SECRET_KEY='testing_key',
        SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI',
                                          'sqlite://'),
        TEST_USER_EMAIL='test_user@example.com',
        TEST_USER_PASSWORD='test_password',
        TESTING=True,
        WTF_CSRF_ENABLED=False,
    )
    FlaskCLI(base_app)
    Babel(base_app)
    Mail(base_app)
    Menu(base_app)
    InvenioDB(base_app)
    InvenioAccounts(base_app)
    base_app.register_blueprint(blueprint)

    with base_app.app_context():
        if str(db.engine.url) != "sqlite://" and \
           not database_exists(str(db.engine.url)):
            create_database(str(db.engine.url))
        db.drop_all()
        db.create_all()

    def teardown():
        drop_database(str(db.engine.url))
        shutil.rmtree(instance_path)

    return base_app


@pytest.fixture
def app(base_app):
    InvenioUserProfiles(base_app)
    return base_app
