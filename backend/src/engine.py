import datetime as dt

from sqlalchemy import desc, cast, Date

from backend.src.auth import Auth
from backend.src.model.hamster import Fact
from backend.src.model.mysql import db, User, Activity, Task, HashTag, Project


class Engine(object):
    def __init__(self):
        self.user = Auth.get_request_user()

    def __get_task_by_external_id(self, external_task_id=None, project_name=None):
        if external_task_id is None:
            return None
        task = db.session.query(Task).filter(Task.external_task_id == external_task_id).first()  # type:Task
        if task is None:
            project = None
            if project_name is not None:
                project = self.__get_project_by_name(project_name) or self.__get_project_by_code(project_name)
                if project is None:
                    project = Project(title=project_name)
                    project.users.append(self.user)
            task = Task(external_task_id=external_task_id)
            if project is not None:
                task.project = project
            db.session.add(task)
            db.session.commit()

        return task

    def __get_project_by_name(self, project_name):
        return db.session.query(Project) \
            .join(User.projects) \
            .filter(Project.title == project_name) \
            .filter(User.id == self.user.id) \
            .first()

    def __get_project_by_code(self, project_code):
        return db.session.query(Project) \
            .join(User.projects) \
            .filter(Project.code == project_code) \
            .filter(User.id == self.user.id) \
            .first()

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
            return 'Не заполнена обязательная часть:\n' \
                   '[время] [номер_задачи] имя_активности[@проект] [#тег], [#тег2], [описание]'
        if self.user is None:
            return 'нет пользователя с таким токеном'
        new_activity = Activity()
        new_activity.time_start = fact.start_time or dt.datetime.now()
        new_activity.time_end = fact.end_time
        new_activity.name = fact.get_task_name()
        new_activity.update_hashtags(fact.tags)
        new_activity.comment = fact.description
        new_activity.user = self.user
        new_activity.task = self.__get_task_by_external_id(fact.get_task_id(), fact.category)
        new_activity.last_updated = dt.datetime.now()

        # закрываем текущую активность, если есть
        # время завершения = время начала новой
        current = self.get_current()  # type:Activity
        if current is not None:
            current.stop(new_activity.time_start)

        db.session.add(new_activity)
        return True

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
            return 'Такой активности не существует'
        if fact.start_time is None:
            return 'Не заполнено время начала активности'
        external_task_id = fact.get_task_id()
        if external_task_id is None:
            return 'не указан номер задачи'
        task = self.__get_task_by_external_id(external_task_id)
        db_fact.time_start = fact.start_time
        db_fact.time_end = fact.end_time
        db_fact.name = fact.get_task_name()
        db_fact.task_id = task.id
        db_fact.comment = fact.description
        db_fact.update_hashtags(fact.tags)
        db.session.add(db_fact)
        return True
