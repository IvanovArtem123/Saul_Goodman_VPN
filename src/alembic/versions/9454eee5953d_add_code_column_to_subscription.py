"""Add code column to subscription

Revision ID: 9454eee5953d
Revises: 6ecac3c4fa32
Create Date: 2026-04-27 20:35:00.895306

"""
from typing import Union, Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9454eee5953d'
down_revision: Union[str, Sequence[str], None] = '6ecac3c4fa32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Добавляем колонку code в subscription (сначала nullable)
    with op.batch_alter_table('subscription') as batch_op:
        batch_op.add_column(sa.Column('code', sa.String(length=16), nullable=True))
    
    # Заполняем существующие записи уникальными значениями
    op.execute("UPDATE subscription SET code = hex(randomblob(8)) WHERE code IS NULL")
    
    # Делаем колонку NOT NULL и добавляем unique constraint
    with op.batch_alter_table('subscription') as batch_op:
        batch_op.alter_column('code', nullable=False)
        batch_op.create_unique_constraint('uq_subscription_code', ['code'])
    
    # Добавляем unique constraints для таблицы user
    with op.batch_alter_table('user') as batch_op:
        batch_op.create_unique_constraint('uq_user_tg_id', ['tg_id'])
        batch_op.create_unique_constraint('uq_user_uuid', ['uuid'])
        batch_op.create_unique_constraint('uq_user_password_hash', ['password_hash'])
        batch_op.create_unique_constraint('uq_user_username', ['username'])


def downgrade() -> None:
    """Downgrade schema."""
    # Удаляем constraints из таблицы user
    with op.batch_alter_table('user') as batch_op:
        batch_op.drop_constraint('uq_user_username', type_='unique')
        batch_op.drop_constraint('uq_user_password_hash', type_='unique')
        batch_op.drop_constraint('uq_user_uuid', type_='unique')
        batch_op.drop_constraint('uq_user_tg_id', type_='unique')
    
    # Удаляем колонку из subscription
    with op.batch_alter_table('subscription') as batch_op:
        batch_op.drop_constraint('uq_subscription_code', type_='unique')
        batch_op.drop_column('code')