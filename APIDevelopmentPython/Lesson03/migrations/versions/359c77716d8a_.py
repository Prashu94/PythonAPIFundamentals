"""empty message

Revision ID: 359c77716d8a
Revises: bf7348487705
Create Date: 2022-04-07 20:17:14.722220

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '359c77716d8a'
down_revision = 'bf7348487705'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('bio', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'bio')
    # ### end Alembic commands ###
