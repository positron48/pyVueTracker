from datetime import date, datetime
import re

from backend.src.auth import Auth
from backend.src.model.hamster import Fact, FormattedFact
from backend.src.model.mysql import db, User, Activity, Task, HashTag, Project
from sqlalchemy import desc, cast, Date


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

    def get_autocomplete(self, text):
        result = []
        db_facts = None
        if text is None or True:
            db_facts = db.session.query(Activity) \
                .filter(Activity.user_id == self.user.id) \
                .order_by(desc(Activity.time_start)) \
                .limit(15) \
                .all()
        else:
            pass  # todo тут будет парсинг текста для умного автокомплита
        for db_fact in db_facts:  # type: Activity
            result.append(Fact(db_fact).as_text())

        if len(result) == 0:
            return None

        return result

    def add_fact(self, fact: Fact):
        """
        Добавляет факт в БД, добавляет недостающие теги, проставляет связи
        :param fact:
        :return:
        """
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
        new_activity.last_updated = datetime.now()

        # tags
        if fact.tags is not None:
            tags = db.session.query(HashTag).filter(HashTag.name.in_(fact.tags)).all()

            tag_names = set()
            for tag in tags:
                tag_names.add(tag.name)
                new_activity.hashtags.append(tag)

            new_tags = set(fact.tags) - tag_names
            for tag in new_tags:
                new_activity.hashtags.append(HashTag(name=tag))

        db.session.add(new_activity)
        db.session.commit()
        return True, None

    def get_current(self):
        current = db.session.query(Activity) \
            .filter(Activity.user_id == self.user.id) \
            .filter(cast(Activity.time_start, Date) == date.today()) \
            .filter(Activity.time_end.is_(None)) \
            .order_by(desc(Activity.time_start)) \
            .first()
        if current is None:
            return None
        return FormattedFact(current)

    def get_facts(self, dateFrom, dateTo):
        facts = db.session.query(Activity) \
            .filter(Activity.user_id == self.user.id) \
            .filter(Activity.time_start.between(dateFrom, dateTo)) \
            .all()
        return [FormattedFact(fact) for fact in facts]
