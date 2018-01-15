"""Added email confirmation fields

Revision ID: 531817e7f8d3
Revises: 187c01ba4bf7
Create Date: 2017-12-25 21:53:25.102957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '531817e7f8d3'
down_revision = '187c01ba4bf7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###