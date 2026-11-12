# SPDX-FileCopyrightText: 2026 CERN.
# SPDX-License-Identifier: MIT

"""Tests for re-authentication before changing the email address."""

import re

import pytest
from flask import url_for
from helpers import login, sign_up
from invenio_accounts.models import User


@pytest.fixture(scope="module")
def app_config(app_config):
    """Enable re-authentication."""
    app_config["ACCOUNTS_REAUTH_ENABLED"] = True
    return app_config


def _profile_data(app, **kwargs):
    data = dict(
        username="test",
        full_name="Test User",
        affiliations="",
        email=app.config["TEST_USER_EMAIL"],
        email_repeat=app.config["TEST_USER_EMAIL"],
    )
    data.update(kwargs)
    data = {f"profile-{k}": v for k, v in data.items()}
    data["submit"] = "profile"
    return data


def _reauth(app, client):
    mail = app.extensions["mail"]
    with app.test_request_context():
        reauth_url = url_for("invenio_accounts.reauth")
    with mail.record_messages() as outbox:
        client.post(reauth_url, data={"action": "send"})
    assert len(outbox) == 1
    # the code goes to the current address
    assert outbox[0].recipients == [app.config["TEST_USER_EMAIL"]]
    code = re.search(r"\b(\d{6})\b", outbox[0].body).group(1)
    res = client.post(reauth_url, data={"action": "verify", "verify-code": code})
    assert res.status_code == 302


def _current_email(app):
    with app.app_context():
        return User.query.one().email


def test_change_email_requires_reauth(app):
    with app.test_request_context():
        profile_url = url_for("invenio_userprofiles.profile")

    with app.test_client() as client:
        sign_up(app, client)
        login(app, client)

        data = _profile_data(app, email="new@ex.org", email_repeat="new@ex.org")
        res = client.post(profile_url, data=data)
        assert res.status_code == 302
        assert "/account/settings/reauth" in res.location
        assert _current_email(app) == app.config["TEST_USER_EMAIL"]

        _reauth(app, client)
        res = client.post(profile_url, data=data)
        assert res.status_code == 303
        assert _current_email(app) == "new@ex.org"


def test_profile_change_without_email_change_needs_no_reauth(app):
    with app.test_request_context():
        profile_url = url_for("invenio_userprofiles.profile")

    with app.test_client() as client:
        sign_up(app, client)
        login(app, client)

        res = client.post(profile_url, data=_profile_data(app, full_name="New Name"))
        assert res.status_code == 303
        with app.app_context():
            assert User.query.one().user_profile["full_name"] == "New Name"
