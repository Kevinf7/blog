"""image

Revision ID: 852c3a8ce909
Revises: ba26220c5a24
Create Date: 2019-05-02 20:23:28.913451

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '852c3a8ce909'
down_revision = 'ba26220c5a24'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=120), nullable=False),
    sa.Column('thumbnail', sa.String(length=120), nullable=False),
    sa.Column('file_size', sa.Integer(), nullable=False),
    sa.Column('file_width', sa.Integer(), nullable=False),
    sa.Column('file_height', sa.Integer(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('post', 'post',
               existing_type=mysql.VARCHAR(length=15000),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('post', 'post',
               existing_type=mysql.VARCHAR(length=15000),
               nullable=True)
    op.drop_table('images')
    # ### end Alembic commands ###
