"""Creating a transaction balance column

Revision ID: 4a92f0c4ba79
Revises: bf35fe9750dc
Create Date: 2023-09-20 12:23:03.682317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a92f0c4ba79'
down_revision = 'bf35fe9750dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('balance', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction', schema=None) as batch_op:
        batch_op.drop_column('balance')

    # ### end Alembic commands ###
