"""empty message

Revision ID: 8639605fb3f8
Revises: c7ce4da4ea78
Create Date: 2019-01-10 15:25:34.513277

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8639605fb3f8'
down_revision = 'c7ce4da4ea78'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_projects')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_projects',
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('project_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('aliases', mysql.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], name='user_projects_ibfk_2'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='user_projects_ibfk_1'),
    sa.PrimaryKeyConstraint('user_id', 'project_id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
