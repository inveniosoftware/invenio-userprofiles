from invenio_db import db

from invenio_userprofiles.models import UserProfileMixin


class UserProfile(UserProfileMixin, db.Model):
    """ Default UserProfile object"""
