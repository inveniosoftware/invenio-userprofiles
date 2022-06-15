# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Create userprofiles tables."""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c25ef2c50ffa"
down_revision = "71634726ec7e"
branch_labels = ()
depends_on = "9848d0149abd"


def upgrade():
    """Upgrade database."""
    op.create_table(
        "userprofiles_userprofile",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=True),
        sa.Column("displayname", sa.String(length=255), nullable=True),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["accounts_user.id"],
        ),
        sa.PrimaryKeyConstraint("user_id"),
        sa.UniqueConstraint("username"),
    )


def downgrade():
    """Downgrade database."""
    op.drop_table("userprofiles_userprofile")
