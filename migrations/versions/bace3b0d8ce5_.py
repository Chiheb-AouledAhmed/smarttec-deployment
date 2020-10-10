"""empty message

Revision ID: bace3b0d8ce5
Revises: c037256e84bc
Create Date: 2020-10-10 11:13:11.464678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bace3b0d8ce5'
down_revision = 'c037256e84bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscription',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Test_score', sa.Integer(), nullable=True),
    sa.Column('Certif_ref', sa.String(), nullable=True),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.Column('date_certif', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('payment_method', sa.String(length=20), nullable=False),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subscription')
    # ### end Alembic commands ###