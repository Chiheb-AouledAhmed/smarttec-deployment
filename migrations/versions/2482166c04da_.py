"""empty message

Revision ID: 2482166c04da
Revises: d59e23505029
Create Date: 2020-10-07 11:06:05.010461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2482166c04da'
down_revision = 'd59e23505029'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subscription', 'Certif_ref')
    op.add_column('subscription', sa.Column(
        'Certif_ref', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('document', 'title',
                    existing_type=sa.VARCHAR(length=200),
                    nullable=True)
    # ### end Alembic commands ###
