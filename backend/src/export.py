from typing import Union, Sequence, List, Optional, Any
from backend.src.model.mysql import db, User, TrackerUserLink, Activity, Task
from .model.tracker import Activity as extActivity
from .model.tracker import Tracker as TrackerInterface
from .model.tracker import Activity as TrackerActivity
from .engine import Engine


class Export:
    def __init__(self, activity: extActivity, link: TrackerUserLink):
        self.link = link
        self.activity = activity
        self.api = None  # type:TrackerInterface
        self.engine = None  # type: Engine
        self.user = None  # type:User
        self.db_activities = None  # type: Optional[List[Activity]]
        self.ext_activities = None  # type: Optional[List[TrackerActivity]]

    def __dump_db_activities(self):
        from .model.mysql import ActivitySchema
        schema = ActivitySchema(many=True)
        result = schema.dump(self.db_activities).data
        return result

    def __dump_user(self):
        from .model.mysql import UserSchema
        schema = UserSchema()
        result = schema.dump(self.user).data
        return result

    def __dump_ext_activities(self):
        return [item.__dict__ for item in self.ext_activities]

    def __project_activities(self, activities, project_id):
        result = []
        for activity in activities:
            ext_project_id = None
            if isinstance(activity, TrackerActivity):
                ext_project_id = activity.project_id
            if isinstance(activity, Activity):
                props = activity.task.project.tracker_properties
                ext_project_id = activity.task.project.tracker_properties
            if ext_project_id == project_id:
                result.append(activity)
        return result

    def init(self):
        if self.activity is None:
            return 'Активность не передана'
        if self.activity.date is None:
            return 'Не задана дата активности'
        if self.activity.time is None:
            return 'Не задано время активности'
        if self.link is None:
            return 'Трекер не найден'
        if self.api is None:
            self.api = TrackerInterface.get_api(self.link.tracker.type, self.link.tracker.api_url,
                                                api_key=self.link.external_api_key)
            if self.api is None:
                return 'Подходящий движок не найден'
            if not self.api.is_auth():
                return 'Учетные данные не приняты трекером'
        if self.engine is None:
            self.engine = Engine()
        if self.user is None:
            self.user = self.engine.user  # type:User
        if self.db_activities is None:
            self.db_activities = self.engine.get_closed_facts_by_date(self.activity.date)
            if self.db_activities is None:
                return 'Активности в БД не найдено'
            self.db_activities = self.__project_activities(self.db_activities, self.activity.project_id)

        # запрашиваем список внешних активностей на эту дату, с привязкой к пользователю
        if self.ext_activities is None:
            user_id = None
            #user_id = self.link.external_user_id
            self.ext_activities = self.api.list_activities_in_date(self.activity.date, user_id=user_id)
            if self.ext_activities is None:
                return 'Ошибка внешнего api'
            self.ext_activities = self.__project_activities(self.ext_activities, self.activity.project_id)
        return True

    def get_status(self):
        # если внешних активностей на эту дату нет - считаем активность новой
        if len(self.ext_activities) == 0:
            return 'new'

        result = {
            'debug': {
                'type': self.api.get_tracker_type(),
                'db': self.__dump_db_activities(),
                'ext': self.__dump_ext_activities(),
                'user': self.__dump_user(),
                'activity': self.activity.__dict__,
            }
        }
        return result
        for item in self.db_activities:
            return item.__dict__.items()
