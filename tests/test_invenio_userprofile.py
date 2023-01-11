# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Module tests."""

import pytest
from flask import Flask
from flask_mail import Mail
from flask_menu import Menu
from invenio_accounts import InvenioAccounts
from invenio_db import InvenioDB, db
from invenio_i18n import Babel

from invenio_userprofiles import InvenioUserProfiles


def test_version():
    """Test version import."""
    from invenio_userprofiles import __version__

    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask("testapp")
    app.config.update(
        ACCOUNTS_USE_CELERY=False,
        SECRET_KEY="test_key",
    )
    Babel(app)
    Mail(app)
    Menu(app)
    InvenioDB(app)
    InvenioAccounts(app)
    ext = InvenioUserProfiles(app)
    assert "invenio-userprofiles" in app.extensions

    app = Flask("testapp")
    app.config.update(
        ACCOUNTS_USE_CELERY=False,
        SECRET_KEY="test_key",
    )
    Babel(app)
    Mail(app)
    Menu(app)
    InvenioDB(app)
    InvenioAccounts(app)
    ext = InvenioUserProfiles()
    assert "invenio-userprofiles" not in app.extensions
    ext.init_app(app)
    assert "invenio-userprofiles" in app.extensions


def test_alembic(app):
    """Test alembic recipes."""
    ext = app.extensions["invenio-db"]

    with app.app_context():
        if db.engine.name == "sqlite":
            raise pytest.skip("Upgrades are not supported on SQLite.")

        assert not ext.alembic.compare_metadata()
        db.drop_all()
        ext.alembic.upgrade()

        assert not ext.alembic.compare_metadata()
        ext.alembic.downgrade(target="96e796392533")
        ext.alembic.upgrade()

        assert not ext.alembic.compare_metadata()
        ext.alembic.downgrade(target="96e796392533")
