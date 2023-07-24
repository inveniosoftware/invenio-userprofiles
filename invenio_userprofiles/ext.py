# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""User profiles module for Invenio."""

from . import config
from .api import current_userprofile
from .forms import confirm_register_form_factory, register_form_factory


class InvenioUserProfiles(object):
    """Invenio-UserProfiles extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)

        # Register current_profile
        app.context_processor(lambda: dict(current_userprofile=current_userprofile))

        app.extensions["invenio-userprofiles"] = self

    def init_config(self, app):
        """Initialize configuration."""
        excludes = [
            "USERPROFILES_BASE_TEMPLATE",
            "USERPROFILES_SETTINGS_TEMPLATE",
        ]
        for k in dir(config):
            if k.startswith("USERPROFILES_") and k not in excludes:
                app.config.setdefault(k, getattr(config, k))

        app.config.setdefault("USERPROFILES", True)

        app.config.setdefault(
            "USERPROFILES_BASE_TEMPLATE",
            app.config.get("BASE_TEMPLATE", "invenio_userprofiles/base.html"),
        )

        app.config.setdefault(
            "USERPROFILES_SETTINGS_TEMPLATE",
            app.config.get(
                "SETTINGS_TEMPLATE", "invenio_userprofiles/settings/base.html"
            ),
        )

        if app.config["USERPROFILES_EXTEND_SECURITY_FORMS"]:
            app.config.setdefault(
                "USERPROFILES_REGISTER_USER_BASE_TEMPLATE",
                app.config.get(
                    "SECURITY_REGISTER_USER_TEMPLATE",
                    "invenio_accounts/register_user.html",
                ),
            )

            app.config["SECURITY_REGISTER_USER_TEMPLATE"] = (
                "invenio_userprofiles/register_user.html"
            )


def finalize_app(app):
    """Finalize app.

    NOTE: replace former @record_once decorator
    """
    init_common(app)


def api_finalize_app(app):
    """Finalize app for api.

    NOTE: replace former @record_once decorator
    """
    init_common(app)


def init_common(app):
    """Post initialization."""
    if app.config["USERPROFILES_EXTEND_SECURITY_FORMS"]:
        security_ext = app.extensions["security"]
        security_ext.confirm_register_form = confirm_register_form_factory(
            security_ext.confirm_register_form
        )
        security_ext.register_form = register_form_factory(security_ext.register_form)
