# SPDX-FileCopyrightText: 2015-2026 CERN.
# SPDX-License-Identifier: MIT

"""Helper functions for tests."""

from flask import url_for
from invenio_accounts.testutils import reauth_user_via_session


def sign_up(app, client, email=None, password=None):
    """Register a user."""
    with app.test_request_context():
        register_url = url_for("security.register")

    res = client.post(
        register_url,
        data=dict(
            email=email or app.config["TEST_USER_EMAIL"],
            password=password or app.config["TEST_USER_PASSWORD"],
        ),
        environ_base={"REMOTE_ADDR": "127.0.0.1"},
    )
    assert res.status_code == 302  # redirect after signedup


def login(app, client, email=None, password=None, reauth=True):
    """Log the user in with the test client.

    :param reauth: Also mark the user as freshly re-authenticated, so views
        asking for a confirmation code can be used right away.
    """
    with app.test_request_context():
        login_url = url_for("security.login")

    res = client.post(
        login_url,
        data=dict(
            email=email or app.config["TEST_USER_EMAIL"],
            password=password or app.config["TEST_USER_PASSWORD"],
        ),
    )
    assert res.status_code == 302  # redirect after login
    if reauth:
        reauth_user_via_session(client)
