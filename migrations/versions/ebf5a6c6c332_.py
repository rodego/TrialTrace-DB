"""empty message

Revision ID: ebf5a6c6c332
Revises: 09f37a26e0f9
Create Date: 2021-02-24 13:14:54.746440

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebf5a6c6c332'
down_revision = '09f37a26e0f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fields', sa.Column('field_meta', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('fields', 'field_meta')
    # ### end Alembic commands ###
