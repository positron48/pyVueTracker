"""empty message

Revision ID: 78c5c4ef77ab
Revises: 6d4534801245
Create Date: 2019-03-01 11:27:38.348330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78c5c4ef77ab'
down_revision = '6d4534801245'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # удаляем внешние ключи
    op.drop_constraint('tracker_projects_ibfk_1', 'tracker_projects', type_='foreignkey')
    op.drop_constraint('tracker_projects_ibfk_2', 'tracker_projects', type_='foreignkey')
    op.drop_constraint('tracker_projects_ibfk_3', 'tracker_projects', type_='foreignkey')
    # дропаем PK
    op.execute('ALTER TABLE tracker_projects DROP PRIMARY KEY')
    # возвращаем внешние ключи
    op.create_foreign_key(None, 'tracker_projects', 'projects', ['project_id'], ['id'])
    op.create_foreign_key(None, 'tracker_projects', 'trackers', ['tracker_id'], ['id'])
    op.create_foreign_key(None, 'tracker_projects', 'users', ['user_id'], ['id'])
    # возвращаем PK
    op.create_primary_key('pk_tracker_projects', 'tracker_projects', ['tracker_id', 'project_id', 'user_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # удаляем внешние ключи
    op.drop_constraint('tracker_projects_ibfk_1', 'tracker_projects', type_='foreignkey')
    op.drop_constraint('tracker_projects_ibfk_2', 'tracker_projects', type_='foreignkey')
    op.drop_constraint('tracker_projects_ibfk_3', 'tracker_projects', type_='foreignkey')
    # дропаем PK
    op.execute('ALTER TABLE tracker_projects DROP PRIMARY KEY')
    # возвращаем PK
    op.create_primary_key('pk_tracker_projects', 'tracker_projects', ['tracker_id', 'project_id'])
    # возвращаем внешние ключи
    op.create_foreign_key(None, 'tracker_projects', 'projects', ['project_id'], ['id'])
    op.create_foreign_key(None, 'tracker_projects', 'trackers', ['tracker_id'], ['id'])
    op.create_foreign_key(None, 'tracker_projects', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###
