from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()


########################################### Сущности: ##################################################################

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), unique=True, nullable=False)
    hash = db.Column(db.String(255), nullable=False)
    last_login = db.Column(db.DateTime)

    projects = db.relationship('Project', back_populates='users', secondary='user_projects')

    def __init__(self, login=None, hash=None):
        self.login = login
        self.hash = hash

    def __repr__(self):
        return 'User: %r' % self.login


class AuthToken(db.Model):
    __tablename__ = 'auth_tokens'
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    value = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    last_used = db.Column(db.DateTime)
    expires = db.Column(db.DateTime)


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    code = db.Column(db.String(255))

    users = db.relationship('User', back_populates='projects', secondary='user_projects')
    properties = db.relationship('Property', secondary='project_properties')

    def __init__(self, title=None, code=None):
        self.title = title
        self.code = code

    def __repr__(self):
        return 'Project: %r' % self.title


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey(Project.id))
    title = db.Column(db.String(255))

    properties = db.relationship('Property', secondary='task_properties')

    def __init__(self, title=None):
        self.title = title


class Tracker(db.Model):
    __tablename__ = 'trackers'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    code = db.Column(db.String(255))
    ui_url = db.Column(db.String(255))
    api_url = db.Column(db.String(255), nullable=False)

    properties = db.relationship('Property', secondary='tracker_properties')

    def __init__(self, title=None, code=None, url=None, base_url=None):
        self.title = title
        self.code = code
        self.ui_url = url
        self.api_url = base_url


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    tracker_id = db.Column(db.Integer, db.ForeignKey(Tracker.id))
    title = db.Column(db.String(255))
    code = db.Column(db.String(255))
    external_category_id = db.Column(db.Integer, nullable=False)

    def __init__(self, title=None, code=None, id=None):
        self.title = title
        self.code = code
        self.external_category_id = id

class PropType(db.Model):
    __tablename__ = 'property_types'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    code = db.Column(db.String(255), nullable=False)

    def __init__(self, code, title=None):
        self.code = code
        self.title = title


class Property(db.Model):
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey(PropType.id), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    title = db.Column(db.String(255))
    code = db.Column(db.String(255))
    value = db.Column(db.String(255))

    def __init__(self, title=None, code=None, value=None):
        self.title = title
        self.code = code
        self.value = value

class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    task_id = db.Column(db.Integer, db.ForeignKey(Task.id))
    name = db.Column(db.String(255))
    comment = db.Column(db.String(255))
    time_start = db.Column(db.DateTime)
    time_end = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean, default=False)
    last_updated = db.Column(db.DateTime)
    version = db.Column(db.Integer, default=0)

    properties = db.relationship('Property', secondary='activity_properties')

    def __init__(self, name=None, comment=None, time_start=None):
        self.name = name
        self.comment = comment
        self.time_start = time_start

class HashTag(db.Model):
    __tablename__ = 'hashtags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)

    def __init__(self, name=None):
        self.name = name


########################################### MTM: #######################################################################

user_projects_table = db.Table('user_projects', db.metadata,
                               db.Column('user_id', db.Integer, db.ForeignKey(User.id), primary_key=True),
                               db.Column('project_id', db.Integer, db.ForeignKey(Project.id), primary_key=True)
                               )

project_properties_table = db.Table('project_properties', db.metadata,
                                    db.Column('project_id', db.Integer, db.ForeignKey(Project.id), primary_key=True),
                                    db.Column('property_id', db.Integer, db.ForeignKey(Property.id), primary_key=True)
                                    )

activity_properties_table = db.Table('activity_properties', db.metadata,
                                     db.Column('activity_id', db.Integer, db.ForeignKey(Activity.id), primary_key=True),
                                     db.Column('property_id', db.Integer, db.ForeignKey(Property.id), primary_key=True)
                                     )

task_properties_table = db.Table('task_properties', db.metadata,
                                 db.Column('task_id', db.Integer, db.ForeignKey(Task.id), primary_key=True),
                                 db.Column('property_id', db.Integer, db.ForeignKey(Property.id), primary_key=True)
                                 )

tracker_properties_table = db.Table('tracker_properties', db.metadata,
                                    db.Column('tracker_id', db.Integer, db.ForeignKey(Tracker.id), primary_key=True),
                                    db.Column('property_id', db.Integer, db.ForeignKey(Property.id), primary_key=True)
                                    )

########################################### MTM extra fields: ##########################################################

'''
class SqliteMapping(db.Model):
    __tablename__ = 'sqlite_project_mapping'
    project_id = db.Column(db.Integer, db.ForeignKey(Project.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    alias = db.Column(db.String(255), primary_key=True)


class ActivityHashtag(db.Model):
    __tablename__ = 'activity_hashtags'
    activity_id = db.Column(db.Integer, db.ForeignKey(Activity.id), primary_key=True)
    hashtag_id = db.Column(db.Integer, db.ForeignKey(HashTag.id), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))


class TrackerAuth(db.Model):
    __tablename__ = 'tracker_auth'
    tracker_id = db.Column(db.Integer, db.ForeignKey(Tracker.id), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    external_login = db.Column(db.String(255))
    external_password = db.Column(db.String(255))


class TrackerUser(db.Model):
    __tablename__ = 'tracker_users'
    tracker_id = db.Column(db.Integer, db.ForeignKey(Tracker.id), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    external_api_key = db.Column(db.String(255))
    external_user_id = db.Column(db.String(255))


class TrackerTask(db.Model):
    __tablename__ = 'tracker_tasks'
    tracker_id = db.Column(db.Integer, db.ForeignKey(Tracker.id), primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey(Task.id), primary_key=True)
    external_task_id = db.Column(db.Integer)
    external_task_title = db.Column(db.String(255))


class TrackerProject(db.Model):
    __tablename__ = 'tracker_projects'
    tracker_id = db.Column(db.Integer, db.ForeignKey(Tracker.id), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey(Project.id), primary_key=True)
    external_project_id = db.Column(db.Integer)
    external_project_title = db.Column(db.String(255))


class TrackerActivity(db.Model):
    __tablename__ = 'tracker_activities'
    tracker_id = db.Column(db.Integer, db.ForeignKey(Tracker.id), primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey(Activity.id), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id))
    external_activity_id = db.Column(db.Integer)
    external_activity_title = db.Column(db.String(255))
    external_version = db.Column(db.Integer)
'''

########################################### fulltext index: ############################################################
'''
db.Index('project_name', Project.title, mysql_prefix='FULLTEXT')
db.Index('activity_comment', Activity.comment, mysql_prefix='FULLTEXT')
db.Index('activity_name', Activity.name, mysql_prefix='FULLTEXT')
db.Index('hashtag_name', HashTag.name, mysql_prefix='FULLTEXT')
'''
