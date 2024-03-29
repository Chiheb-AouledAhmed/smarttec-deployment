"""empty message

Revision ID: d59e23505029
Revises: a8ccb5b87433
Create Date: 2020-10-07 10:38:42.973390

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd59e23505029'
down_revision = 'a8ccb5b87433'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('document', sa.Column(
        'title', sa.String(length=200), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('document', 'title')
    # ### end Alembic commands ###
