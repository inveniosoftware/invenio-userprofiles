# SPDX-FileCopyrightText: 2026 CERN.
# SPDX-License-Identifier: MIT

"""Test the alembic recipe that moves the user profiles to the users."""

import importlib.util
from pathlib import Path

import sqlalchemy as sa
from alembic.operations import Operations
from alembic.runtime.migration import MigrationContext
from invenio_accounts.models import User
from invenio_db import db

import invenio_userprofiles


def test_remove_table_moves_the_profiles(app):
    """Quotes, colons and missing usernames survive the move."""
    folder = Path(invenio_userprofiles.__file__).parent / "alembic"
    spec = importlib.util.spec_from_file_location(
        "remove_table", next(folder.glob("41157f1933d6_*.py"))
    )
    recipe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(recipe)
    profiles = [("dellolio", "Domenico Dell'Olio"), (None, "Jean :Paul"), (None, "X")]

    with app.app_context():
        users = [User(email=f"{i}@test.org", active=True) for i in range(3)]
        db.session.add_all(users)
        db.session.commit()
        ids = [user.id for user in users]

        connection = db.session.connection()
        with Operations.context(MigrationContext.configure(connection)):
            recipe.downgrade()  # the table as before the recipe
            for user_id, (username, full_name) in zip(ids, profiles):
                connection.execute(
                    sa.text(
                        "INSERT INTO userprofiles_userprofile (user_id, username, "
                        "displayname, full_name) VALUES (:id, :name, :name, :full)"
                    ),
                    {"id": user_id, "name": username, "full": full_name},
                )
            recipe.upgrade()
        db.session.commit()

        table = User.__table__
        rows = db.session.execute(
            sa.select(table.c.username, table.c.displayname, table.c.profile)
            .where(table.c.id.in_(ids))
            .order_by(table.c.id)
        ).all()
        assert [tuple(row) for row in rows] == [
            (username, username, {"full_name": full_name})
            for username, full_name in profiles
        ]
        assert not sa.inspect(db.engine).has_table("userprofiles_userprofile")
