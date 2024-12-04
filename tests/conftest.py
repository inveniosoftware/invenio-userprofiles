# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
# Copyright (C) 2022-2024 Graz University of Technology.
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
from flask_webpackext.manifest import (
    JinjaManifest,
    JinjaManifestEntry,
    JinjaManifestLoader,
)
from invenio_accounts import InvenioAccounts
from invenio_accounts.views.settings import (
    create_settings_blueprint as create_accounts_blueprint,
)
from invenio_assets import InvenioAssets
from invenio_db import InvenioDB, db
from invenio_i18n import Babel, InvenioI18N
from sqlalchemy_utils.functions import create_database, database_exists, drop_database

from invenio_userprofiles import InvenioUserProfiles
from invenio_userprofiles.ext import finalize_app
from invenio_userprofiles.views import create_blueprint


#
# Mock the webpack manifest to avoid having to compile the full assets.
#
class MockJinjaManifest(JinjaManifest):
    """Mock manifest."""

    def __getitem__(self, key):
        """Get a manifest entry."""
        return JinjaManifestEntry(key, [key])

    def __getattr__(self, name):
        """Get a manifest entry."""
        return JinjaManifestEntry(name, [name])


class MockManifestLoader(JinjaManifestLoader):
    """Manifest loader creating a mocked manifest."""

    def load(self, filepath):
        """Load the manifest."""
        return MockJinjaManifest()


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
        ACCOUNTS_BASE_TEMPLATE="invenio_accounts/base.html",
        ACCOUNTS_COVER_TEMPLATE="invenio_accounts/base_cover.html",
        WEBPACKEXT_MANIFEST_LOADER=MockManifestLoader,
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
    InvenioI18N(base_app)
    InvenioAssets(base_app)
    base_app.register_blueprint(create_accounts_blueprint(base_app))

    with base_app.app_context():
        if str(
            db.engine.url.render_as_string(hide_password=False)
        ) != "sqlite://" and not database_exists(
            str(db.engine.url.render_as_string(hide_password=False))
        ):
            create_database(str(db.engine.url.render_as_string(hide_password=False)))
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
        drop_database(str(db.engine.url.render_as_string(hide_password=False)))
    shutil.rmtree(instance_path)


def _init_userprofiles_app(app_):
    """Init UserProfiles modules."""
    InvenioUserProfiles(app_)
    app_.register_blueprint(create_blueprint(app_))
    with app_.app_context():
        finalize_app(app_)
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
