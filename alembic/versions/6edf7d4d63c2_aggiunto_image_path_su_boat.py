"""aggiunto image_path su boat

Revision ID: 6edf7d4d63c2
Revises: a18004f3f519
Create Date: 2025-03-29 17:07:03.723404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6edf7d4d63c2'
down_revision: Union[str, None] = 'a18004f3f519'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('boats', sa.Column('image_path', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('boats', 'image_path')
    # ### end Alembic commands ###
