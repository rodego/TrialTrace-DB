"""empty message

Revision ID: 8cdeca2046df
Revises: c57c264039ff
Create Date: 2021-02-23 17:20:28.167085

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8cdeca2046df'
down_revision = 'c57c264039ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fields',
    sa.Column('field_uid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('field_name', sa.Text(), nullable=True),
    sa.Column('field_note', sa.Text(), nullable=True),
    sa.Column('field_source', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('field_depends_on', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['users.user_uid'], ),
    sa.ForeignKeyConstraint(['field_depends_on'], ['data.datum_uid'], ),
    sa.PrimaryKeyConstraint('field_uid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fields')
    # ### end Alembic commands ###