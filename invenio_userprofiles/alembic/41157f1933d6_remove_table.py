#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
# Copyright (C)      2022 Graz University of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Remove table."""

import json

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "41157f1933d6"
down_revision = "c25ef2c50ffa"
branch_labels = ()
depends_on = "eb9743315a9d"  # invenio-accounts: add_userprofile


def upgrade():
    """Upgrade database."""
    # Migrate username and full_name to invenio_accounts table.
    connection = op.get_bind()
    results = connection.execute(
        "SELECT user_id, username, displayname, full_name "
        "FROM userprofiles_userprofile;"
    ).all()

    for r in results:
        user_id, username, displayname, full_name = r
        profile_data = {
            "full_name": full_name,
        }
        preferences = {"visibility": "restricted", "email_visibility": "restricted"}

        query = (
            "UPDATE accounts_user SET "
            " username = '{username}', "
            " displayname = '{displayname}', "
            " profile = '{profile_data_string}', "
            " preferences = '{preferences}' "
            "WHERE accounts_user.id = {user_id};".format(
                username=username,
                displayname=displayname,
                profile_data_string=json.dumps(profile_data),
                preferences=json.dumps(preferences),
                user_id=user_id,
            )
        )
        op.execute(query)

    op.drop_table("userprofiles_userprofile")


def downgrade():
    """Downgrade database."""
    op.create_table(
        "userprofiles_userprofile",
        sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "username", sa.VARCHAR(length=255), autoincrement=False, nullable=True
        ),
        sa.Column(
            "displayname", sa.VARCHAR(length=255), autoincrement=False, nullable=True
        ),
        sa.Column(
            "full_name", sa.VARCHAR(length=255), autoincrement=False, nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["accounts_user.id"],
            name="fk_userprofiles_userprofile_user_id_accounts_user",
        ),
        sa.PrimaryKeyConstraint("user_id", name="pk_userprofiles_userprofile"),
        sa.UniqueConstraint("username", name="uq_userprofiles_userprofile_username"),
    )
