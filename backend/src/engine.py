import datetime as dt
import re

from backend.src.auth import Auth
from backend.src.model.hamster import Fact, FormattedFact
from backend.src.model.mysql import db, User, Activity, Task, HashTag, Project
from sqlalchemy import desc, cast, Date
from sqlalchemy.orm.session import make_transient


class Engine(object):
    def __init__(self):
        self.user = Auth.get_request_user()

    @staticmethod
    def __get_task_by_external_id(external_task_id):
        return db.session.query(Task.id).filter(Task.external_task_id == external_task_id).first()

    def __get_project_by_name(self, project_name):
        return db.session.query(Project.id) \
            .join(User.projects) \
            .filter(Project.title == project_name) \
            .filter(User.id == self.user.id).first()

    def __get_project_by_code(self, project_code):
        return db.session.query(Project.id) \
            .join(User.projects) \
            .filter(Project.code == project_code) \
            .filter(User.id == self.user.id).first()

    def __get_hashtags(self, tag_names):
        result = db.session.query(HashTag).filter(HashTag.name.in_(tag_names)).all()
        db_tag_names = {tag.name for tag in result}
        new_tag_names = set(tag_names) - db_tag_names
        for name in new_tag_names:
            hashtag = HashTag(name=name)
            result.append(hashtag)
            db.session.add(hashtag)
        return result

    def __get_fact_by_id(self, id: int):
        if id < 1:
            return None
        return db.session.query(Activity) \
            .filter(Activity.user_id == self.user.id) \
            .filter(Activity.id == id) \
            .first()  # type:Activity

    def get_autocomplete(self, text):
        db_facts = None
        if text is None or True:
            db_facts = db.session.query(Activity) \
                .filter(Activity.user_id == self.user.id) \
                .order_by(desc(Activity.time_start)) \
                .limit(15) \
                .all()
        else:
            pass  # todo тут будет парсинг текста для умного автокомплита
        return db_facts

    def add_fact(self, fact: Fact):
        if not fact.validate():
            return False, 'Не заполнена обязательная часть:\n' \
                          'время номер_задачи [имя_активности][@проект] [#тег], [#тег2], [описание]'

        new_activity = Activity()

        # user
        if self.user is None:
            return False, 'нет пользователя с таким токеном'
        new_activity.user_id = self.user.id

        # task_id
        external_task_id = fact.get_task_id()
        if external_task_id is None:
            return False, 'не указан номер задачи'
        task = self.__get_task_by_external_id(external_task_id)
        if task is None:
            if fact.category is None:
                return False, 'не указан проект для новой задачи'
            project = self.__get_project_by_name(fact.category)
            if project is None:
                project = self.__get_project_by_code(fact.category)
            if project is None:
                return False, 'среди ваших проектов нет проекта ' + fact.category
            task = Task(external_task_id=external_task_id, project_id=project.id)
            db.session.add(task)
            db.session.commit()
        new_activity.task_id = task.id

        # name
        name = re.findall('^\d*\s*(.*)', fact.activity)
        if name is not False and name != '' and name is not None:
            new_activity.name = name.pop().strip()

        # comment
        if fact.description is not None:
            new_activity.comment = fact.description

        # time_start
        new_activity.time_start = fact.start_time

        # time_end
        if fact.end_time is not None:
            new_activity.time_end = fact.end_time

        # last_updated
        new_activity.last_updated = dt.datetime.now()

        # tags
        new_activity.update_hashtags(fact.tags)

        db.session.add(new_activity)
        # закрываем текущую активность, если есть
        current = self.get_current()  # type:Activity
        if current is not None:
            current.stop()
        return True, None

    def get_current(self):
        current = db.session.query(Activity) \
            .filter(Activity.user_id == self.user.id) \
            .filter(cast(Activity.time_start, Date) == dt.date.today()) \
            .filter(Activity.time_end.is_(None)) \
            .order_by(desc(Activity.time_start)) \
            .first()
        return current

    def get_facts(self, dateFrom, dateTo):
        facts = db.session.query(Activity) \
            .filter(Activity.user_id == self.user.id) \
            .filter(cast(Activity.time_start, Date) >= dateFrom) \
            .filter(cast(Activity.time_start, Date) <= dateTo) \
            .all()
        return facts

    def delete_fact(self, id: int):
        if id < 1:
            return False
        fact = db.session.query(Activity) \
            .filter(Activity.user_id == self.user.id) \
            .filter(Activity.id == id) \
            .first()
        if fact is None:
            return False
        db.session.delete(fact)
        return True

    def stop_fact(self, id):
        fact = self.__get_fact_by_id(id)  # type:Activity
        if fact is None:
            return False
        fact.stop()
        return True

    def resume_fact(self, id):
        fact = self.__get_fact_by_id(id)  # type:Activity
        if fact is None:
            return False
        # закрываем текущую активность, если есть
        current = self.get_current()  # type:Activity
        if current is not None:
            current.stop()
        fact.resume()
        return True

    def edit_fact(self, id, fact: Fact):
        db_fact = self.__get_fact_by_id(int(id))  # type:Activity
        if db_fact is None:
            return False, 'Такой активности не существует'
        if fact.start_time is None:
            return False, 'Не заполнено время начала активности'
        external_task_id = fact.get_task_id()
        if external_task_id is None:
            return False, 'не указан номер задачи'
        task = self.__get_task_by_external_id(external_task_id)
        if task is None:
            if fact.category is None:
                return False, 'не указан проект для новой задачи'
            project = self.__get_project_by_name(fact.category)
            if project is None:
                project = self.__get_project_by_code(fact.category)
            if project is None:
                return False, 'среди ваших проектов нет проекта ' + fact.category
            task = Task(external_task_id=external_task_id, project_id=project.id)
            db.session.add(task)
            db.session.commit()
        db_fact.time_start = fact.start_time
        db_fact.time_end = fact.end_time
        db_fact.name = fact.get_task_name()
        db_fact.task_id = task.id
        db_fact.comment = fact.description
        db_fact.update_hashtags(fact.tags)
        db.session.add(db_fact)
        return True, None
