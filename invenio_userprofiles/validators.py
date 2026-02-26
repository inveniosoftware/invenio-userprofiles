# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2026 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Validators for user profiles."""

import re
import warnings

from invenio_i18n import lazy_gettext as _

username_regex = re.compile("^[a-zA-Z][a-zA-Z0-9-_]{2}[a-zA-Z0-9-_]*$")
"""Deprecated. Use the `ACCOUNTS_USERNAME_REGEX` config variable in invenio_accounts instead.

Username rules."""

USERNAME_RULES = _(
    "Username must start with a letter, be at least three characters long and"
    " only contain alphanumeric characters, dashes and underscores."
)
"""Deprecated. Use the `ACCOUNTS_USERNAME_RULES_TEXT` config variable in invenio_accounts instead.

Description of username validation rules.

.. note:: Used for both form help text and for form validation error."""


def validate_username(username):
    """Deprecated. Use invenio_accounts.utils.validate_username instead.

    Validate the username.

    See :data:`~.username_regex` to know which rules are applied.

    :param username: A username.
    :raises ValueError: If validation fails.
    """
    warnings.warn(
        "invenio_userprofiles.validators.validate_username is deprecated and will be removed in "
        "a future release. Please use invenio_accounts.utils.validate_username instead.",
        DeprecationWarning,
    )
    if not username_regex.match(username):
        raise ValueError(USERNAME_RULES)
