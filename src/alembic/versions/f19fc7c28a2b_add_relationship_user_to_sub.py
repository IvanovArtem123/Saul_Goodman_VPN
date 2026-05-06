"""Add relationship user to sub

Revision ID: f19fc7c28a2b
Revises: cd6f33e6fef8
Create Date: 2026-05-03 21:10:18.149961

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f19fc7c28a2b'
down_revision: Union[str, Sequence[str], None] = 'cd6f33e6fef8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        'subscription_panels_subscription_id_fkey', 
        'subscription_panels', 
        type_='foreignkey'
    )
    op.create_foreign_key(
        'subscription_panels_subscription_id_fkey',
        'subscription_panels', 'subscription',
        ['subscription_id'], ['id'],
        ondelete='CASCADE'
    )

def downgrade() -> None:
    op.drop_constraint(
        'subscription_panels_subscription_id_fkey', 
        'subscription_panels', 
        type_='foreignkey'
    )
    op.create_foreign_key(
        'subscription_panels_subscription_id_fkey',
        'subscription_panels', 'subscription',
        ['subscription_id'], ['id']
    )
