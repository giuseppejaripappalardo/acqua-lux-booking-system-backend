"""aggiunti campi per refund e price_difference in bookings

Revision ID: a18004f3f519
Revises: 0d5854077637
Create Date: 2025-03-25 21:55:40.463064

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a18004f3f519'
down_revision: Union[str, None] = '0d5854077637'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookings', sa.Column('price_difference', sa.DECIMAL(precision=10, scale=2), nullable=True))
    op.add_column('bookings', sa.Column('requires_refund', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bookings', 'requires_refund')
    op.drop_column('bookings', 'price_difference')
    # ### end Alembic commands ###
