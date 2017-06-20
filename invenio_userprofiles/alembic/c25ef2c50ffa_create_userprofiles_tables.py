#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Create userprofiles tables."""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'c25ef2c50ffa'
down_revision = '71634726ec7e'
branch_labels = ()
depends_on = '9848d0149abd'


def upgrade():
    """Upgrade database."""
    op.create_table(
        'userprofiles_userprofile',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=255), nullable=True),
        sa.Column('displayname', sa.String(length=255), nullable=True),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], [u'accounts_user.id'], ),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('username')
    )


def downgrade():
    """Downgrade database."""
    op.drop_table('userprofiles_userprofile')
