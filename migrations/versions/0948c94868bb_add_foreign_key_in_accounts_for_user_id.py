"""Add foreign key in Accounts for user.id

Revision ID: 0948c94868bb
Revises: 780ef1d5ff60
Create Date: 2024-12-25 23:19:36.819879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0948c94868bb'
down_revision = '780ef1d5ff60'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('accounts', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('accounts', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
