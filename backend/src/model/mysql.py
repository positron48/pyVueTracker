from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from marshmallow_sqlalchemy import ModelConverter as ModelSchema
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

    trackers = db.relationship(lambda: Tracker, secondary='tracker_users')
    projects = db.relationship(lambda: TrackerProjectLink)
    settings = db.relationship(lambda: UserSettings)

    def __repr__(self):
        return 'User: %r' % self.login


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    code = db.Column(db.String(255))

    tracker_properties = db.relationship(lambda: TrackerProjectLink)

    def __repr__(self):
        return 'Project: %r' % self.title


class Tracker(db.Model):
    __tablename__ = 'trackers'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    code = db.Column(db.String(255))
    type = db.Column(db.String(255))
    ui_url = db.Column(db.String(255))  # для генерации ссылок вида https://redmine.skillum.ru/issues/55597
    api_url = db.Column(db.String(255), nullable=False)
    last_sync = db.Column(db.DateTime)  # по этой метке раз в сутки синхронизируем словари категорий и проектов

    users = db.relationship(User, secondary='tracker_users')
    properties = db.relationship(lambda: TrackerUserLink)
    categories = db.relationship(lambda: Category)


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey(Project.id))
    tracker_id = db.Column(db.Integer, db.ForeignKey(Tracker.id))
    title = db.Column(db.String(255))
    external_task_id = db.Column(db.Integer)

    project = db.relationship(lambda: Project)
    tracker = db.relationship(lambda: Tracker)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    tracker_id = db.Column(db.Integer, db.ForeignKey(Tracker.id))
    name = db.Column(db.String(255))
    external_id = db.Column(db.Integer)

    tracker = db.relationship(lambda: Tracker)
    activities = db.relationship(lambda: Activity, secondary='activity_categories')


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    task_id = db.Column(db.Integer, db.ForeignKey(Task.id))
    uploaded = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(255))
    comment = db.Column(db.String(255))
    time_start = db.Column(db.DateTime)
    time_end = db.Column(db.DateTime)

    user = db.relationship(lambda: User)
    task = db.relationship(lambda: Task)
    hashtags = db.relationship(lambda: HashTag, secondary='activity_hashtags')
    categories = db.relationship(lambda: Category, secondary='activity_categories')

    @staticmethod
    def get_hashtags(tag_names):
        if tag_names is None:
            return None
        return db.session.query(HashTag).filter(HashTag.name.in_(tag_names)).all()

    def update_hashtags(self, tag_names):
        if tag_names is None:
            return
        tag_names = {tag.strip() for tag in tag_names if tag.strip()}
        tags = set(tag_names)
        db_tags = self.get_hashtags(tag_names)
        old_tags = {tag.name for tag in self.hashtags}
        del_tags = old_tags - tags
        new_tags = tags - old_tags - {tag.name for tag in db_tags}
        upd_tags = {tag for tag in db_tags if tag.name not in del_tags and tag.name not in new_tags}
        insert = {self.hashtags.append(HashTag(name=name)) for name in new_tags}
        update = {self.hashtags.append(tag) for tag in upd_tags}
        remove = {self.hashtags.remove(tag) for tag in self.hashtags if tag.name in del_tags}

    def stop(self, time_end=None):
        if time_end is None:
            time_end = dt.datetime.now().replace(second=0, microsecond=0)

        self.time_end = time_end
        # если закрыть активность в течении минуты - она считается ошибочной, и удаляется
        if self.time_end - self.time_start < dt.timedelta(minutes=1):
            db.session.delete(self)
        else:
            db.session.add(self)

    def resume(self):
        tags = self.hashtags
        db.session.expunge(self)
        make_transient(self)
        self.id = self.time_end = None
        self.time_start = dt.datetime.now().replace(second=0, microsecond=0)
        db.session.add(self)
        db.session.commit()
        for tag in tags:
            self.hashtags.append(tag)
        db.session.add(self)
        db.session.commit()


class UserSettings(db.Model):
    __tablename__ = 'user_settings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    code = db.Column(db.String(255))
    value = db.Column(db.String(255))

    user = db.relationship(lambda: User)


class HashTag(db.Model):
    __tablename__ = 'hashtags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)

    activities = db.relationship(Activity, secondary='activity_hashtags')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


########################################### MTM: #######################################################################
'''sqlalchemy требует объявлять все таблицы явно, даже связи'''

activity_hashtags_table = db.Table('activity_hashtags', db.metadata,
                                   db.Column('activity_id', db.Integer, db.ForeignKey(Activity.id), primary_key=True),
                                   db.Column('hashtag_id', db.Integer, db.ForeignKey(HashTag.id), primary_key=True)
                                   )

activity_categories_table = db.Table('activity_categories', db.metadata,
                                     db.Column('activity_id', db.Integer, db.ForeignKey(Activity.id), primary_key=True),
                                     db.Column('category_id', db.Integer, db.ForeignKey(Category.id), primary_key=True)
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
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)

    # автозаполняемые справочники
    external_project_id = db.Column(db.Integer)
    external_project_title = db.Column(db.String(255))

    tracker = db.relationship(Tracker)
    project = db.relationship(Project)
    user = db.relationship(User)


########################################### fulltext index: ############################################################

db.Index('project_name', Project.title, mysql_prefix='FULLTEXT')
db.Index('activity_comment', Activity.comment, mysql_prefix='FULLTEXT')
db.Index('activity_name', Activity.name, mysql_prefix='FULLTEXT')
db.Index('hashtag_name', HashTag.name, mysql_prefix='FULLTEXT')


################################################# schema: ##############################################################

# Schema - модуль дампа оъектов моделей, позволяет преобразовать объект модели в словарь, его можно отправить как json
#
# Пример использования:
# from .model.mysql import ActivitySchema
# schema = ActivitySchema()
# fact = db.session.query(Activity).filter(Activity.user_id == self.user.id).first()
# result = schema.dump(fact).data
# return jsonify(result)
#
# Для списков:
# from .model.mysql import ActivitySchema
# schema = ActivitySchema(many=True) #флаг many обрабатывает списки объектов
# facts = db.session.query(Activity).filter(Activity.user_id == self.user.id).all()
# result = schema.dump(facts).data
# return jsonify(result)

class UserSchema(ModelSchema):
    class Meta:
        model = User


class ProjectSchema(ModelSchema):
    class Meta:
        model = Project


class TrackerSchema(ModelSchema):
    class Meta:
        model = Tracker


class TaskSchema(ModelSchema):
    class Meta:
        model = Task


class CategorySchema(ModelSchema):
    class Meta:
        model = Category


class ActivitySchema(ModelSchema):
    class Meta:
        model = Activity


class UserSettingsSchema(ModelSchema):
    class Meta:
        model = UserSettings


class HashTagSchema(ModelSchema):
    class Meta:
        model = HashTag


class TrackerUserLinkSchema(ModelSchema):
    class Meta:
        model = TrackerUserLink


class TrackerProjectLinkSchema(ModelSchema):
    class Meta:
        model = TrackerProjectLink
