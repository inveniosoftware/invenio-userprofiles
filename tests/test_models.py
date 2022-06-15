# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Tests for user profile models."""

import pytest
from invenio_accounts.models import User
from invenio_db import db
from sqlalchemy.exc import IntegrityError
from test_validators import test_usernames

from invenio_userprofiles import InvenioUserProfiles, UserProfile


def test_userprofiles(app):
    """Test UserProfile model."""
    profile = UserProfile(User())

    # Check the username validator works on the model
    profile.username = test_usernames["valid"]
    with pytest.raises(ValueError):
        profile.username = test_usernames["invalid_characters"]
    with pytest.raises(ValueError):
        profile.username = test_usernames["invalid_begins_with_number"]

    # Test non-validated attributes
    profile.first_name = "Test"
    profile.last_name = "User"
    assert profile.first_name == "Test"
    assert profile.last_name == "User"


def test_case_insensitive_username(app):
    """Test case-insensitive uniqueness."""
    with app.app_context():
        with db.session.begin_nested():
            u1 = User(email="test@test.org", username="INFO")
            db.session.add(u1)
        u2 = User(email="test2@test.org", username="info")
        db.session.add(u2)
        pytest.raises(IntegrityError, db.session.commit)


def test_case_preserving_username(app):
    """Test that username preserves the case."""
    with app.app_context():
        with db.session.begin_nested():
            u1 = User(email="test@test.org", username="InFo")
            db.session.add(u1)
        db.session.commit()
        profile = UserProfile.get_by_username("info")
        assert profile.username == "InFo"


def test_delete_cascade(app):
    """Test that deletion of user, also removes profile."""
    with app.app_context():
        with db.session.begin_nested():
            u = User(email="test@test.org", username="InFo")
            db.session.add(u)
        db.session.commit()

        assert UserProfile.get_by_userid(u.id) is not None
        db.session.delete(u)
        db.session.commit()

        assert UserProfile.get_by_userid(u.id) is None
