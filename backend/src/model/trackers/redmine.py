from ..tracker import *
from typing import Union, Sequence, List, Optional, Any
import datetime as dt
from redminelib import Redmine as RedmineLib
from redminelib.exceptions import AuthError, ResourceNotFoundError, ForbiddenError


class Redmine(Tracker):
    def __init__(self, url, token=None, login=None,
                 password=None):
        if token is None and (login is None or password is None):
            raise AttributeError
        self.api = None  # type: RedmineLib
        if token is None:
            self.api = RedmineLib(url, username=login.encode('utf-8'), password=password.encode('utf-8'))
        else:
            self.api = RedmineLib(url, key=token)
        self.auth = self.__is_auth()

    def __is_auth(self) -> bool:
        try:
            auth = self.api.auth()
        except AuthError:
            auth = None
        return auth is not None

    @staticmethod
    def as_dict(obj):
        return obj.__dict__.get('_decoded_attrs')

    def res_to_list(self, res) -> List[Any]:
        return [self.as_dict(item) for item in res if res is not None and item is not None]

    def __get_project(self, id_or_code):
        if self.auth:
            try:
                project = self.api.project.get(id_or_code)
            except ResourceNotFoundError:
                return None
            return Project(id=project.id, code=project.identifier, name=project.name)

    def __filter_activities(self, filter) -> Optional[List[Activity]]:
        if self.auth:
            try:
                activities = self.api.time_entry.filter(**filter)
            except ResourceNotFoundError:
                return None
            return [Activity(id=activity.id, user_id=activity.user.id,
                             date=activity.spent_on, time=activity.hours, task_id=activity.issue.id,
                             comment=activity.comments, category_id=activity.activity.id) for activity in activities]

    ######################################### Tracker interface ########################################################

    def is_auth(self) -> bool:
        """
        Проверяет, авторизован ли пользователь на трекере
        """
        return self.auth

    def get_api_key(self) -> Optional[str]:
        """
        Получает api_key пользователя для трекера, если трекер имеет такую возможность
        :return: возвращает api_key или None
        """
        if self.auth:
            return self.api.auth().api_key

    def get_user_id(self) -> Optional[int]:
        """
        Получает id пользователя на трекере, если он авторизован
        :return: возвращает user_id или None
        """
        if self.auth:
            return self.api.auth().id

    def list_categories(self) -> Optional[List[Category]]:
        """
        Запрашивает список категорий активностей у трекера
        :return: возвращает список категорий или None
        """
        if self.auth:
            categories = self.api.enumeration.filter(resource='time_entry_activities')
            categories = self.res_to_list(categories)
            return [Category(id=category['id'], name=category['name'], default=category.get('is_default', False)) for
                    category in categories]

    def list_projects(self) -> Optional[List[Project]]:
        """
        Запрашивает список проектов у трекера
        :return: возвращает список проектов или None
        """
        if self.auth:
            projects = self.api.project.all()
            return [Project(id=project.id, code=project.identifier, name=project.name) for project in projects]

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        """
        Запрашивает у трекера проект по id
        :param project_id: id запрашиваемого проекта
        :return: возвращает Project или None
        """
        return self.__get_project(project_id)

    def get_project_by_code(self, project_code: str) -> Optional[Project]:
        """
        Запрашивает у трекера проект по коду
        :param project_code: code запрашиваемого проекта
        :return: возвращает Project или None
        """
        return self.__get_project(project_code)

    def get_project_by_name(self, project_name: str) -> Optional[Project]:
        """
        Запрашивает у трекера проект по имени
        :param project_name: name запрашиваемого проекта
        :return: возвращает Project или None
        """
        if self.auth:
            for project in self.list_projects():
                if project.name == project_name:
                    return project

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Запрашивает у трекера задачу по id, если задачи поддерживаются трекером
        :param task_id: id запрашиваемой задачи
        :return: возвращает Task или None
        """
        if self.auth:
            try:
                task = self.api.issue.get(task_id)
            except ResourceNotFoundError:
                return None
            return Task(id=task.id, name=task.subject, project_id=task.project.id, status=task.status.name)

    def list_tasks_in_project(self, project_id: int, all: bool = False) -> Optional[List[Task]]:
        """
        Запрашивает у трекера список задач по id проекта, если задачи поддерживаются трекером
        :param project_id: id проекта
        :param all: возвращать все задачи. По-умолчанию возвращает только открытые
        :return: возвращает список задач или None
        """
        if self.auth:
            try:
                if all:
                    tasks = self.api.issue.filter(project_id=project_id, status_id='*')
                else:
                    tasks = self.api.issue.filter(project_id=project_id)
            except ResourceNotFoundError:
                return None
            return [Task(id=task.id, name=task.subject, project_id=task.project.id, status=task.status.name) for task in
                    tasks]

    def list_activities_in_date(self, date: dt.date) -> Optional[List[Activity]]:
        """
        Запрашивает у трекера список активностей по дате
        :param date: дата
        :return: возвращает список активностей или None
        """
        return self.list_activities_in_date_interval(date, date)

    def list_activities_in_date_interval(self, date_start: dt.date, date_end: dt.date) -> Optional[List[Activity]]:
        """
        Запрашивает у трекера список активностей в интервале дат
        :param date_start: начальная дата
        :param date_end: конечная дата
        :return: возвращает список активностей или None
        """
        return self.__filter_activities({'from_date': date_start, 'to_date': date_end})

    def list_activities_in_task(self, task_id: int) -> Optional[List[Activity]]:
        """
        Запрашивает у трекера список активностей по id задачи, если задачи поддерживаются трекером
        :param task_id: id задачи
        :return: возвращает список активностей или None
        """
        return self.__filter_activities({'issue_id': task_id})

    def list_activities_in_project(self, project_id: int) -> Optional[List[Activity]]:
        """
        Запрашивает у трекера список активностей по id проекта
        :param project_id: id проекта
        :return: возвращает список активностей или None
        """
        return self.__filter_activities({'project_id': project_id})

    def new_activity(self, activity: Activity) -> Optional[int]:
        """
        Создает новую активность на трекере
        :param activity: активность
        :return: возвращает activity_id созданной активности, или None, в случае неудачи
        """
        time_entry = self.api.time_entry.new()
        time_entry.issue_id = activity.task_id
        time_entry.spent_on = activity.date
        time_entry.hours = activity.time
        time_entry.activity_id = activity.category_id
        time_entry.comments = activity.comment
        time_entry.save()
        return time_entry.id

    ######################################### end Tracker interface ####################################################

    def get_all_projects(self):
        return self.api.project.all()

    def get_all_tasks(self):
        return self.api.issue.all()

    def get_api(self):
        return self.api
