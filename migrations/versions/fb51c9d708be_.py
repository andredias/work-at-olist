"""empty message

Revision ID: fb51c9d708be
Revises: 
Create Date: 2018-11-09 20:02:26.177188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb51c9d708be'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('call',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=5), nullable=False),
    sa.Column('call_id', sa.Integer(), nullable=False),
    sa.Column('source', sa.String(length=11), nullable=True),
    sa.Column('destination', sa.String(length=11), nullable=True),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('call')
    # ### end Alembic commands ###