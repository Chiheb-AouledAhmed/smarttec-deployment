"""empty message

Revision ID: 0079f692427e
Revises: 2482166c04da
Create Date: 2020-10-07 11:52:29.031262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0079f692427e'
down_revision = '2482166c04da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subscription') as batch_op:
        batch_op.drop_column('Certif_ref')
    op.add_column('subscription', sa.Column(
        'Certif_ref', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subscription', sa.Column(
        'Certif_ref', sa.INTEGER(), nullable=True))
    # ### end Alembic commands ###
