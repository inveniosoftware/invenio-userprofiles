# SPDX-FileCopyrightText: 2015-2018 CERN.
# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-FileCopyrightText: 2025 KTH Royal Institute of Technology.
# SPDX-License-Identifier: MIT

"""User profiles module for Invenio."""

# Monkey patch Werkzeug 2.1
# Flask-Login uses the safe_str_cmp method which has been removed in Werkzeug
# 2.1. Flask-Login v0.6.0 (yet to be released at the time of writing) fixes the
# issue. Once we depend on Flask-Login v0.6.0 as the minimal version in
# Flask-Security-Invenio/Invenio-Accounts we can remove this patch again.
try:
    # Werkzeug <2.1
    from werkzeug import security

    security.safe_str_cmp
except AttributeError:
    # Werkzeug >=2.1
    import hmac

    from werkzeug import security

    security.safe_str_cmp = hmac.compare_digest

from .api import current_userprofile
from .ext import InvenioUserProfiles
from .models import UserProfile, UserProfileProxy

__version__ = "7.0.0"

__all__ = (
    "__version__",
    "current_userprofile",
    "InvenioUserProfiles",
    "UserProfile",
    "UserProfileProxy",
)
