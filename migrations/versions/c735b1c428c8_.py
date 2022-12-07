"""empty message

Revision ID: c735b1c428c8
Revises: 6e1db9cb0ef0
Create Date: 2022-12-03 10:20:45.142796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c735b1c428c8'
down_revision = '6e1db9cb0ef0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'answer', 'user', ['author_id'], ['id'])
    op.create_foreign_key(None, 'answer', 'question', ['question_id'], ['id'])
    op.create_foreign_key(None, 'question', 'user', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'question', type_='foreignkey')
    op.drop_constraint(None, 'answer', type_='foreignkey')
    op.drop_constraint(None, 'answer', type_='foreignkey')
    # ### end Alembic commands ###