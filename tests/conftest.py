# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
# Copyright (C)      2022 Graz University of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Pytest configuration."""

import os
import shutil
import tempfile

import pytest
from flask import Flask
from flask_mail import Mail
from flask_menu import Menu
from invenio_accounts import InvenioAccounts
from invenio_accounts.views import blueprint as accounts_blueprint
from invenio_db import InvenioDB, db
from invenio_i18n import Babel
from sqlalchemy_utils.functions import create_database, database_exists, drop_database

from invenio_userprofiles import InvenioUserProfiles
from invenio_userprofiles.views import blueprint_ui_init


@pytest.fixture(scope="module")
def app_config(app_config):
    """Override pytest-invenio app_config fixture."""
    app_config.update(
        ACCOUNTS_LOCAL_LOGIN_ENABLED=True,
        ACCOUNTS_USE_CELERY=False,
        LOGIN_DISABLED=False,
        SECRET_KEY="testing_key",
        SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite://"),
        TEST_USER_EMAIL="test_user@test.org",
        TEST_USER_PASSWORD="test_password",
        TEST_USER_USERNAME="test",
        TESTING=True,
        WTF_CSRF_ENABLED=False,
    )

    return app_config


@pytest.fixture()
def base_app(app_config):
    """Flask application fixture."""
    instance_path = tempfile.mkdtemp()
    base_app = Flask(__name__, instance_path=instance_path)
    base_app.config.update(app_config)

    Babel(base_app)
    Mail(base_app)
    Menu(base_app)
    InvenioDB(base_app)
    InvenioAccounts(base_app)
    base_app.register_blueprint(accounts_blueprint)

    with base_app.app_context():
        if str(db.engine.url) != "sqlite://" and not database_exists(
            str(db.engine.url)
        ):
            create_database(str(db.engine.url))
        db.create_all()

    # Taken from: https://github.com/inveniosoftware/invenio-accounts/blob/3ecc1a70da3636618fe14ff2ebf754eed9ec75a1/tests/conftest.py#L94-L112
    def delete_user_from_cache(exception):
        """Delete user from `flask.g` when the request is tearing down.

        Flask-login==0.6.2 changed the way the user is saved i.e uses `flask.g`.
        Flask.g is pointing to the application context which is initialized per
        request. That said, `pytest-flask` is pushing an application context on each
        test initialization that causes problems as subsequent requests during a test
        are detecting the active application request and not popping it when the
        sub-request is tearing down. That causes the logged in user to remain cached
        for the whole duration of the test. To fix this, we add an explicit teardown
        handler that will pop out the logged in user in each request and it will force
        the user to be loaded each time.
        """
        from flask import g

        if "_login_user" in g:
            del g._login_user

    base_app.teardown_request(delete_user_from_cache)

    yield base_app

    with base_app.app_context():
        drop_database(str(db.engine.url))
    shutil.rmtree(instance_path)


def _init_userprofiles_app(app_):
    """Init UserProfiles modules."""
    InvenioUserProfiles(app_)
    app_.register_blueprint(blueprint_ui_init)
    return app_


@pytest.fixture
def app(base_app):
    """Flask application."""
    return _init_userprofiles_app(base_app)


@pytest.fixture
def app_with_csrf(base_app):
    """Flask application with CSRF security enabled."""
    base_app.config.update(
        WTF_CSRF_ENABLED=True,
    )
    return _init_userprofiles_app(base_app)
