import datetime as dt

from sqlalchemy import desc, cast, Date, update

from backend.src.auth import Auth
from backend.src.model.hamster import Fact
from backend.src.model.mysql import db, User, Activity, Task, HashTag, Project, Tracker, TrackerUserLink


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

    def __get_task_by_name(self, external_task_id, task_name, project_name=None):
        if task_name is None:
            return None

        project = None
        if project_name is not None:
            project = self.__get_project_by_name(project_name) or self.__get_project_by_code(project_name)
            if project is None:
                project = Project(title=project_name)
                project.users.append(self.user)

        task = db.session.query(Task).filter(Task.title == task_name) \
            .filter(Task.project_id == project.id).first()  # type:Task

        if task is None:

            task = Task(external_task_id=external_task_id, title=task_name)
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
        # new_activity.task = self.__get_task_by_external_id(fact.get_task_id(), fact.category)
        new_activity.task = self.__get_task_by_name(fact.get_task_id(), fact.get_task_name(), fact.category)
        new_activity.last_updated = dt.datetime.now()

        current = self.get_current()  # type:Activity
        if current is not None:
            # проверяем, чтобы время начала новой активности было не раньше времени начала текущей активности
            if current.time_start > new_activity.time_start:
                return 'Новая активность начинается раньше текущей.\n' \
                       'Исправьте время начала новой активности,\n' \
                       'или удалите/отредактируйте текущую активность.'
            # закрываем текущую активность, время завершения = время начала новой
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

    def get_trackers(self):
        trackers = db.session.query(Tracker, TrackerUserLink) \
            .join(TrackerUserLink) \
            .filter(Tracker.id == TrackerUserLink.tracker_id) \
            .filter(TrackerUserLink.user_id == self.user.id) \
            .all()
        return trackers

    def get_evo_tracker(self):
        tracker = db.session.query(Tracker, TrackerUserLink) \
            .join(TrackerUserLink) \
            .filter(Tracker.type == 'evo') \
            .filter(TrackerUserLink.user_id == self.user.id) \
            .first()
        return tracker

    def save_tracker(self, id, type, title, api_url):
        # если трекер привязан только к текущему пользователю, разрешаем его изменять
        tracker = None
        if id is not None and int(id) > 0:
            tracker = db.session.query(Tracker).filter(Tracker.id == id).first()

        if tracker is None:
            tracker = db.session.query(Tracker).filter(Tracker.api_url == api_url).first()

        if tracker is None:
            tracker = Tracker(type=type, title=title, api_url=api_url)
            db.session.add(tracker)
        else:
            if len(tracker.users) == 1 and self.user in tracker.users:
                tracker.title = title
                tracker.api_url = api_url

        if self.user not in tracker.users:
            tracker_link = TrackerUserLink(tracker=tracker, user=self.user)
            db.session.add(tracker_link)

        db.session.commit()

        return True

    def save_user_id(self, tracker_id, user_id):
        tracker_link = db.session.query(TrackerUserLink) \
            .filter(TrackerUserLink.tracker_id == tracker_id) \
            .filter(TrackerUserLink.user_id == self.user.id).first()

        if tracker_link is not None:
            tracker_link.external_user_id = user_id
            db.session.commit()
        else:
            return False

        return True

    def delete_tracker(self, id):
        # если трекер привязан только к текущему пользователю, удаляем кго полностью
        # если трекер привязан к нескольким пользователям, удаляем привязку к текущему пользователю
        tracker = None
        if id is not None and int(id) > 0:
            tracker = db.session.query(Tracker).filter(Tracker.id == id).first()

        if tracker is not None and self.user in tracker.users:
            tracker_link = db.session.query(TrackerUserLink) \
                .filter(TrackerUserLink.user_id == self.user.id) \
                .filter(TrackerUserLink.tracker_id == tracker.id) \
                .first()
            db.session.delete(tracker_link)

        if len(tracker.users) == 1 and self.user in tracker.users:
            db.session.delete(tracker)

        db.session.commit()

        return True

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

        task = self.__get_task_by_name(external_task_id, fact.get_task_name(), fact.category)
        db_fact.time_start = fact.start_time
        db_fact.time_end = fact.end_time
        db_fact.name = fact.get_task_name()
        db_fact.task_id = task.id
        db_fact.comment = fact.description
        db_fact.update_hashtags(fact.tags)
        db.session.add(db_fact)
        return True

    def get_tracker(self, tracker_id):
        tracker = db.session.query(Tracker) \
            .filter(Tracker.id == tracker_id) \
            .first()

        return tracker

    def set_api_key(self, tracker_id, token):
        tracker_link = db.session.query(TrackerUserLink) \
            .filter(TrackerUserLink.tracker_id == tracker_id) \
            .filter(TrackerUserLink.user_id == self.user.id) \
            .first()

        if tracker_link is not None:
            tracker_link.external_api_key = token
            db.session.commit()
            return True

        return False