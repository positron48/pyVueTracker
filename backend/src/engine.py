import datetime as dt
from typing import Union, Sequence, List, Optional

from sqlalchemy import asc, desc, cast, Date, update, func

from backend.src.auth import Auth
from backend.src.model.hamster import Fact
from backend.src.model.mysql import db, User, Activity, Task, HashTag, Project, Tracker, TrackerUserLink, \
    TrackerProjectLink, UserSettings
from .model.tracker import Tracker as TrackerModel
from .model.tracker import Activity as TrackerActivity


class Engine:
    def __init__(self):
        self.user = Auth.get_request_user()

    @staticmethod
    def __get_task_by_external_task_id(external_task_id):
        return db.session.query(Task).filter(Task.external_task_id == external_task_id).first()  # type:Task

    @staticmethod
    def __get_task_by_title(task_name):
        return db.session.query(Task).filter(Task.title == task_name).first()  # type:Task

    @staticmethod
    def __get_task_by_name(task_name, task_category=None):
        if task_category is None:
            return db.session.query(Task).filter(Task.title == task_name).first()  # type:Task
        else:
            return db.session.query(Task).join(Task.project) \
                .filter(Task.title == task_name).filter(Project.title == task_category).first()

    def __get_or_create_project_by_fact(self, fact: Fact):
        project_name = fact.category
        if project_name is None:
            return None
        return self.__get_project_by_name(project_name) or self.__get_project_by_code(project_name) or Project(
            title=project_name)

    def __get_or_create_task_by_fact(self, fact: Fact):
        task_id = fact.get_task_id()
        task_name = fact.get_task_name()
        task_category = fact.get_task_category()

        if task_id is None and task_name is None:
            return None

        task = None  # type:Task
        if task_id is not None:
            task = self.__get_task_by_external_task_id(task_id)
        if task is None:
            task = self.__get_task_by_name(task_name, task_category)
        if task is None:
            task = Task(external_task_id=task_id, title=task_name)

        task.project = self.__get_or_create_project_by_fact(fact)

        db.session.add(task)
        db.session.commit()

        return task

    def __get_project_by_name(self, project_name):
        return db.session.query(Project) \
            .filter(Project.title == project_name) \
            .first()

    def __get_project_by_code(self, project_code):
        return db.session.query(Project) \
            .filter(Project.code == project_code) \
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

    def get_autocomplete(self, text, count=50):
        db_facts = None
        if text is None:
            db_facts = db.session.query(Activity) \
                .filter(Activity.user_id == self.user.id) \
                .order_by(desc(Activity.time_start)) \
                .limit(count) \
                .all()
        else:
            # todo тут будет парсинг текста для умного автокомплита
            db_facts = db.session.query(Activity) \
                .filter(Activity.user_id == self.user.id) \
                .filter(Activity.name.like('%' + text + '%')) \
                .order_by(desc(Activity.time_start)) \
                .limit(count) \
                .all()

        return db_facts

    def add_fact(self, fact: Fact):
        if not fact.validate():
            return 'Введите название задачи'
        if self.user is None:
            return 'Нет пользователя с таким токеном'
        new_activity = Activity()
        new_activity.time_start = fact.start_time or dt.datetime.now().replace(second=0, microsecond=0)
        new_activity.time_end = fact.end_time
        new_activity.name = fact.get_task_name()
        new_activity.update_hashtags(fact.tags)
        new_activity.comment = fact.description
        new_activity.user = self.user
        new_activity.task = self.__get_or_create_task_by_fact(fact)

        last = self.get_last()  # type:Activity
        if last is not None:
            # проверяем, чтобы время начала новой активности было не раньше времени начала текущей активности
            if last.time_start <= new_activity.time_start:
                # закрываем текущую активность, время завершения = время начала новой
                if last.time_end is None or last.time_end >= new_activity.time_start:
                    last.stop(new_activity.time_start)
            else:
                # проверка на пересечение с другими активностями
                if not self.check_intervals(new_activity.time_start, new_activity.time_end):
                    return 'Активность пересекается с предыдущими. ' + \
                           'Измените интервал или отредактируйте предыдущие активности'

        db.session.add(new_activity)
        return True

    def check_intervals(self, start, end, exclude_id=None):
        date_start = start.replace(hour=0, minute=0, second=0)  # взять начало дня

        date_end = end
        if date_end is None:
            date_end = dt.datetime.now().replace(second=0, microsecond=0)

        tasks = self.get_facts(date_start, date_end)  # дата окончания или текущая, если нулл

        # проверяем все полученные активности, не пересекается ли одна из них с новой
        for task in tasks:
            if (exclude_id is None) or (task.id != exclude_id):
                if task.time_end is None and end is None:
                    return False

                if self.is_interval_intersect(start, date_end, task.time_start, task.time_end):
                    # print([task.name])
                    # print([start, date_end])
                    # print([task.time_start, task.time_end])
                    return False

        return True

    @staticmethod
    def is_interval_intersect(t1_start, t1_end, t2_start, t2_end):
        if t2_end is None:
            t2_end = dt.datetime.now().replace(second=0, microsecond=0)
        return (t1_start <= t2_start < t1_end) or (t2_start <= t1_start < t2_end)

    def get_current(self):
        current = db.session.query(Activity) \
            .filter(Activity.user_id == self.user.id) \
            .filter(Activity.time_end.is_(None)) \
            .order_by(desc(Activity.time_start)) \
            .first()
        return current

    def get_last(self):
        last = db.session.query(Activity) \
            .filter(Activity.user_id == self.user.id) \
            .filter(cast(Activity.time_start, Date) == dt.date.today()) \
            .order_by(desc(Activity.time_start)) \
            .first()
        return last

    def get_facts(self, date_from, date_to):
        facts = db.session.query(Activity) \
            .filter(Activity.user_id == self.user.id) \
            .filter(Activity.time_start >= date_from) \
            .filter(Activity.time_start <= date_to) \
            .order_by(asc(Activity.time_start)) \
            .all()
        return facts

    def get_trackers(self):
        trackers = db.session.query(Tracker, TrackerUserLink) \
            .join(TrackerUserLink) \
            .filter(Tracker.id == TrackerUserLink.tracker_id) \
            .filter(TrackerUserLink.user_id == self.user.id) \
            .all()
        return trackers

    def get_default_redmine_tracker(self):
        tracker = db.session.query(Tracker) \
            .filter(Tracker.type == 'redmine') \
            .first()
        return tracker

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

    def link_project(self, project_id, tracker_id, tracker_project_id, tracker_project_title):
        link = db.session.query(TrackerProjectLink) \
            .filter(TrackerProjectLink.tracker_id == tracker_id) \
            .filter(TrackerProjectLink.user_id == self.user.id) \
            .filter(TrackerProjectLink.project_id == project_id).first()

        if link is None:
            new_link = TrackerProjectLink(project_id=project_id, tracker_id=tracker_id, user_id=self.user.id)
            db.session.add(new_link)
            link = new_link

        # обновляем данные
        link.external_project_id = tracker_project_id
        link.external_project_title = tracker_project_title

        # применяем изменения
        db.session.commit()

        return True

    def delete_fact(self, id: int):
        if id < 1:
            return False
        fact = db.session.query(Activity) \
            .filter(Activity.user_id == self.user.id) \
            .filter(Activity.id == id) \
            .first()  # type: Activity
        if fact is None:
            return False
        # не разрешаем удалять выгруженные активности
        if not fact.uploaded:
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
        # не даем редактировать выгруженные активности
        if db_fact.uploaded:
            return 'Активность уже выгружена на внешний трекер'
        if fact.start_time is None:
            return 'Не заполнено время начала активности'
        if fact.end_time is not None and fact.end_time <= fact.start_time:
            return 'Время окончания активности меньше, чем время начала'
        if not self.check_intervals(fact.start_time, fact.end_time, int(id)):
            return 'Активность пересекается с предыдущими. ' + \
                   'Измените интервал или отредактируйте предыдущие активности'

        db_fact.time_start = fact.start_time
        db_fact.time_end = fact.end_time
        db_fact.name = fact.get_task_name()
        db_fact.task = self.__get_or_create_task_by_fact(fact)
        db_fact.comment = fact.description
        db_fact.update_hashtags(fact.tags)
        db.session.add(db_fact)
        return True

    def get_tracker_by_id(self, tracker_id) -> Optional[Tracker]:
        return db.session.query(Tracker) \
            .filter(Tracker.id == tracker_id) \
            .first()

    def get_tracker_link(self, tracker_id) -> Optional[TrackerUserLink]:
        return db.session.query(TrackerUserLink) \
            .filter(TrackerUserLink.tracker_id == tracker_id) \
            .filter(TrackerUserLink.user_id == self.user.id) \
            .first()

    def get_user_projects(self):
        return db.session.query(Project.title, func.count(Project.title).label('total')) \
            .join(Task.project) \
            .join(Activity) \
            .filter(Activity.task_id == Task.id) \
            .filter(Activity.user_id == self.user.id) \
            .group_by(Project.title) \
            .order_by(desc(func.count(Project.title))) \
            .all()

    def get_user_tags(self):
        return db.session.query(HashTag.name, func.count(HashTag.name).label('total')) \
            .join(HashTag.activities) \
            .filter(Activity.user_id == self.user.id) \
            .group_by(HashTag.name) \
            .order_by(desc(func.count(HashTag.name))) \
            .all()

    def get_projects(self, project_ids=None):
        if project_ids is None:
            return []

        projects = db.session.query(Project) \
            .filter(Project.id.in_(project_ids)) \
            .all()

        return projects

    def set_api_key(self, tracker_id, token):
        tracker_link = db.session.query(TrackerUserLink) \
            .filter(TrackerUserLink.tracker_id == tracker_id) \
            .filter(TrackerUserLink.user_id == self.user.id) \
            .first()  # type:TrackerUserLink

        if tracker_link is not None:
            tracker_link.external_api_key = token
            # для редмайна обновляем user_id по api, для эво - через фронт
            if tracker_link.tracker.type == 'redmine' and tracker_link.tracker.api_url is not None and tracker_link.external_user_id is None:
                from .model.trackers.redmine import Redmine
                redmine = Redmine(tracker_link.tracker.api_url, token=token)
                tracker_link.external_user_id = redmine.get_user_id()
            db.session.commit()
            return True

        return False

    def get_closed_facts_by_date(self, date: dt.date) -> Optional[List[Activity]]:
        return db.session.query(Activity) \
            .filter(Activity.user_id == self.user.id) \
            .filter(cast(Activity.time_start, Date) == date) \
            .filter(Activity.time_end.isnot(None)) \
            .all()

    def get_closed_facts_by_date_interval(self, date_start: dt.date, date_end: dt.date) -> Optional[List[Activity]]:
        return db.session.query(Activity) \
            .filter(Activity.user_id == self.user.id) \
            .filter(cast(Activity.time_start, Date) >= date_start) \
            .filter(cast(Activity.time_end, Date) <= date_end) \
            .filter(Activity.time_end.isnot(None)) \
            .all()

    def get_tracker_link_by_token(self, token) -> Optional[TrackerUserLink]:
        return db.session.query(TrackerUserLink) \
            .filter(TrackerUserLink.external_api_key == token) \
            .first()

    def get_settings(self):
        current_settings = {}
        for object in self.user.settings:
            current_settings[object.code] = object.value

        return current_settings

    def save_settings(self, settings):
        current_settings = {}
        for object in self.user.settings:
            current_settings[object.code] = object

        for key, value in settings.items():
            if key in current_settings:
                current_settings[key].value = value
            else:
                setting = UserSettings(
                    user_id=self.user.id,
                    code=key,
                    value=value
                )
                db.session.add(setting)

        db.session.commit()

        return True

    def get_task_time_by_date_for_db(self, task_id: int, date: dt.datetime):
        db_activities = self.get_closed_facts_by_date(date)

        if db_activities is None:  # нет активностей по задаче
            return 0

        db_time = 0
        for db_activity in db_activities:  # считаем суммарное время по задаче
            if db_activity.task.external_task_id == task_id:
                db_time += round((db_activity.time_end - db_activity.time_start).total_seconds() / 3600, 2)

        return db_time

    def get_task_time_by_date_for_tracker_link(self, link: TrackerUserLink, task_id: int, date: dt.datetime):
        api = TrackerModel.get_api(link.tracker.type, link.tracker.api_url, link.external_api_key)

        if not api.is_auth():  # нет авторизации на апи
            return None  # ошибка

        ext_activities = api.list_activities_in_date(date, user_id=link.external_user_id)

        if ext_activities is None:  # нет активностей по задаче
            return 0

        ext_time = 0
        for ext_activity in ext_activities:  # считаем суммарное время по задаче
            if ext_activity.task_id == task_id:
                ext_time += ext_activity.time

        return ext_time

    def is_task_uploaded_in_tracker(self, activity_id: int, tracker_id: int):
        activity = self.__get_fact_by_id(activity_id)  # type: Activity
        if activity is None:
            return None

        for tracker in activity.uploaded_trackers:
            if tracker.id == tracker_id:
                return True

        return False

    def export_activity(self, link: TrackerUserLink, activity: TrackerActivity) -> Optional[str]:
        """
        Перед экспортом запрашиваем на трекере время по задаче на дату активности.
        Активностей на трекере нет - выгрузим активность, вернем статус "new".
        Время по задаче совпадает - все уже выгружено, вернем статус "exist".
        Время по задаче в БД больше, чем на трекере - выгрузим активность, вернем статус "new".
        Время по задаче в БД меньше, чем на трекере - не выгружаем, вернем статус "partial". На трекере активности созданы в обход сервиса.
        :param link: TrackerUserLink
        :param activity: TrackerActivity
        :return: [None|'new'|'exist'|'partial']
        """
        if activity.date is None or activity.user_id is None or activity.id is None:
            return None  # ошибка

        db_activity = self.__get_fact_by_id(activity.id)
        if db_activity is None:
            return None  # ошибка


        # убедимся, что активность не выгружена
        if self.is_task_uploaded_in_tracker(activity.id, link.tracker.id):
            return 'exist'

        if activity.task_id > 0:
            # запросим суммарное время по задаче на дату активности у трекера и БД
            ext_time = self.get_task_time_by_date_for_tracker_link(link, activity.task_id, activity.date)
            db_time = activity.time #self.get_task_time_by_date_for_db(activity.task_id, activity.date)

            if abs(db_time - ext_time) < 0.05:  # время совпадает - все активности уже синхронизированы
                return 'exist'

            if db_time < ext_time:  # время в БД меньше, чем на трекере - какая-то активность создана в обход БД
                # todo импортируем активности с трекера в БД?
                return 'partial'

        # время в БД больше, чем на трекере - выгружаем активность
        api = TrackerModel.get_api(link.tracker.type, link.tracker.api_url, link.external_api_key)
        if not api.is_auth():
            return None

        result = api.new_activity(activity)
        if result is None or not result.isnumeric():
            return result  # ошибка

        # проставляем upload_link
        link.tracker.uploaded_activities.append(db_activity)
        db.session.commit()

        return 'new'
