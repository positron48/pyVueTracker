from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from marshmallow_sqlalchemy import ModelSchema
import datetime as dt
from sqlalchemy.orm.session import make_transient

db = SQLAlchemy()


########################################### Сущности: ##################################################################

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), unique=True, nullable=False)
    hash = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    last_login = db.Column(db.DateTime)

    projects = db.relationship(lambda: Project, secondary='user_projects')
    trackers = db.relationship(lambda: Tracker, secondary='tracker_users')

    def __repr__(self):
        return 'User: %r' % self.login


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    code = db.Column(db.String(255))

    users = db.relationship(User, secondary='user_projects')
    tracker_properties = db.relationship(lambda: TrackerProjectLink)
    sqlite_aliases = db.relationship(lambda: UserProjectLink)
    categories = db.relationship(lambda: Category)

    def __repr__(self):
        return 'Project: %r' % self.title


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey(Project.id))
    title = db.Column(db.String(255))
    # автозаполняемые справочники
    external_task_id = db.Column(
        db.Integer)  # redmine_task_id. evo не имеет сущностей task, а redmine пока один - храним id в сущности

    project = db.relationship(lambda: Project)


class Tracker(db.Model):
    __tablename__ = 'trackers'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    code = db.Column(db.String(255))
    type = db.Column(db.String(255))
    ui_url = db.Column(db.String(255))  # для генерации ссылок вида https://redmine.skillum.ru/issues/55597
    api_url = db.Column(db.String(255), nullable=False)

    users = db.relationship(User, secondary='tracker_users')
    properties = db.relationship(lambda: TrackerUserLink)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey(Project.id))
    name = db.Column(db.String(255))
    external_id = db.Column(db.Integer)

    project = db.relationship(lambda: Project)


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    task_id = db.Column(db.Integer, db.ForeignKey(Task.id))
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id))
    name = db.Column(db.String(255))
    comment = db.Column(db.String(255))
    time_start = db.Column(db.DateTime)
    time_end = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean, default=False)
    last_updated = db.Column(db.DateTime)

    task = db.relationship(lambda: Task)
    hashtags = db.relationship(lambda: HashTag, secondary='activity_hashtags')
    category = db.relationship(lambda: Category)

    @staticmethod
    def get_hashtags(tag_names):
        return db.session.query(HashTag).filter(HashTag.name.in_(tag_names)).all()

    def update_hashtags(self, tag_names):
        tags = self.get_hashtags(tag_names)
        for name in set(tag_names) - {tag.name for tag in tags}:
            tag = HashTag(name=name)
            db.session.add(tag)
            tags.append(tag)
        for tag in tags:
            self.hashtags.append(tag)
        return tags

    def stop(self):
        self.time_end = dt.datetime.now()
        # если отменить активность в течении минуты - она удаляется
        if self.time_end - self.time_start < dt.timedelta(minutes=1):
            db.session.delete(self)
        else:
            db.session.add(self)

    def resume(self):
        tags = self.hashtags
        db.session.expunge(self)
        make_transient(self)
        self.id = self.time_end = None
        self.time_start = dt.datetime.now()
        db.session.add(self)
        db.session.commit()
        for tag in tags:
            self.hashtags.append(tag)
        db.session.add(self)
        db.session.commit()


class HashTag(db.Model):
    __tablename__ = 'hashtags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)

    activities = db.relationship(Activity, secondary='activity_hashtags')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Error(db.Model):
    __tablename__ = 'errors'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    type = db.Column(db.String(255))
    target = db.Column(db.String(255))
    data = db.Column(db.Text)


########################################### MTM: #######################################################################
'''sqlalchemy требует объявлять все таблицы явно, даже связи'''

activity_hashtags_table = db.Table('activity_hashtags', db.metadata,
                                   db.Column('activity_id', db.Integer, db.ForeignKey(Activity.id), primary_key=True),
                                   db.Column('hashtag_id', db.Integer, db.ForeignKey(HashTag.id), primary_key=True)
                                   )

########################################### MTM extra fields: ##########################################################
'''как пользоваться extra fields: https://www.pythoncentral.io/sqlalchemy-association-tables/'''


class TrackerUserLink(db.Model):
    __tablename__ = 'tracker_users'
    tracker_id = db.Column(db.Integer, db.ForeignKey(Tracker.id), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    # у одного пользователя на каждом трекере user_id свой
    external_user_id = db.Column(db.Integer)
    # авторизация
    external_api_key = db.Column(db.String(255))

    tracker = db.relationship(Tracker)
    user = db.relationship(User)


class TrackerProjectLink(db.Model):
    __tablename__ = 'tracker_projects'
    tracker_id = db.Column(db.Integer, db.ForeignKey(Tracker.id), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey(Project.id), primary_key=True)
    # автозаполняемые справочники
    external_project_id = db.Column(db.Integer)
    external_project_title = db.Column(db.String(255))
    last_updated = db.Column(db.DateTime)

    tracker = db.relationship(Tracker)
    project = db.relationship(Project)


class UserProjectLink(db.Model):
    __tablename__ = 'user_projects'
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey(Project.id), primary_key=True)
    aliases = db.Column(db.Text)  # список алиасов, для импорта из sqlite

    user = db.relationship(User)
    project = db.relationship(Project)


########################################### fulltext index: ############################################################

db.Index('project_name', Project.title, mysql_prefix='FULLTEXT')
db.Index('activity_comment', Activity.comment, mysql_prefix='FULLTEXT')
db.Index('activity_name', Activity.name, mysql_prefix='FULLTEXT')
db.Index('hashtag_name', HashTag.name, mysql_prefix='FULLTEXT')


################################################# schema: ##############################################################


class ProjectSchema(ModelSchema):
    class Meta(object):
        model = Project


class HashTagSchema(ModelSchema):
    class Meta(object):
        model = HashTag
