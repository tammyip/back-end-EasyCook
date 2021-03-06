"""updates recipe model

Revision ID: cf731db1a9a1
Revises: d625636345a8
Create Date: 2021-08-12 12:42:00.065268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf731db1a9a1'
down_revision = 'd625636345a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipe', sa.Column('plan_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'recipe', 'plan', ['plan_id'], ['plan_id'])
    op.create_unique_constraint(None, 'user', ['user_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'recipe', type_='foreignkey')
    op.drop_column('recipe', 'plan_id')
    # ### end Alembic commands ###
