# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Tests for user profile validators."""

from __future__ import absolute_import, print_function

import pytest

from invenio_userprofiles.validators import validate_username

test_usernames = {
    'valid': 'Good-Name_9',
    'valid_begins_with_number': '9CanStartWithNumber',
    'invalid_characters': '_Containsi!!ega!Char acters*',
    'invalid_short': 'ab',
}


def test_validate_username(app):
    """Test username validator."""
    # Goodname can contain letters and numbers
    validate_username(test_usernames['valid'])
    validate_username(test_usernames['valid_begins_with_number'])

    # Can only contain latin letters and numbers
    with pytest.raises(ValueError):
        validate_username(test_usernames['invalid_characters'])

    with pytest.raises(ValueError):
        validate_username(test_usernames['invalid_short'])
