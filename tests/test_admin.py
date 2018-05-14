# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from flask import Flask, url_for
from flask_admin import Admin
from invenio_admin import InvenioAdmin
from invenio_db import db

from invenio_userprofiles import InvenioUserProfiles
from invenio_userprofiles.admin import UserProfileView, user_profile_adminview


def test_admin(app):
    """Test flask-admin interace."""
    InvenioUserProfiles(app)

    assert isinstance(user_profile_adminview, dict)

    assert 'model' in user_profile_adminview
    assert 'modelview' in user_profile_adminview

    admin = Admin(app, name="Test")

    user_model = user_profile_adminview.pop('model')
    user_view = user_profile_adminview.pop('modelview')
    admin.add_view(user_view(user_model, db.session,
                             **user_profile_adminview))

    with app.test_request_context():
        request_url = url_for('userprofile.index_view')

    with app.app_context():
        with app.test_client() as client:
            res = client.get(
                request_url,
                follow_redirects=True
            )
            assert res.status_code == 200
            assert b'Username' in (res.get_data())
            assert b'Full Name' in (res.get_data())
