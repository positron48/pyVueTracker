from typing import Union, Sequence, List, Optional
import datetime as dt


class User:
    def __init__(self, id: int, name: str = None):
        self.id = id
        self.name = name


class Project:
    def __init__(self, id: int, code: str = None, name: str = None):
        self.id = id
        self.code = code
        self.name = name


class Task:
    def __init__(self, id: int, name: str, project_id: int, project_name: str, tracker_name: str, status: str = None):
        self.id = id
        self.name = name
        self.project_id = project_id
        self.project_name = project_name
        self.tracker_name = tracker_name
        self.status = status


class Category:
    def __init__(self, id: int, name: str, default: bool = False):
        self.id = id
        self.name = name
        self.default = default


class Activity:
    def __init__(self, task_id: int, time: float, date: dt.date, id: int = None, user_id: int = None,
                 comment: str = None,
                 title: str = None, category_id: int = None):
        self.id = id
        self.user_id = user_id
        self.date = date
        self.time = time
        self.task_id = task_id
        self.comment = comment
        self.title = title  # формулировка для эво
        self.category_id = category_id


class Tracker:
    def is_auth(self) -> bool:
        """
        Проверяет, авторизован ли пользователь на трекере
        """
        raise NotImplementedError

    def get_api_key(self) -> Optional[str]:
        """
        Получает api_key пользователя для трекера, если трекер имеет такую возможность
        :return: возвращает api_key или None
        """
        return None

    def get_user_id(self) -> Optional[int]:
        """
        Получает id пользователя на трекере, если он авторизован
        :return: возвращает user_id или None
        """
        return None

    def list_categories(self) -> Optional[List[Category]]:
        """
        Запрашивает список категорий активностей у трекера
        :return: возвращает список категорий или None
        """
        return None

    def list_projects(self) -> Optional[List[Project]]:
        """
        Запрашивает список проектов у трекера
        :return: возвращает список проектов или None
        """
        return None

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        """
        Запрашивает у трекера проект по id
        :param project_id: id запрашиваемого проекта
        :return: возвращает Project или None
        """
        return None

    def get_project_by_code(self, project_code: str) -> Optional[Project]:
        """
        Запрашивает у трекера проект по коду
        :param project_code: code запрашиваемого проекта
        :return: возвращает Project или None
        """
        return None

    def get_project_by_name(self, project_name: str) -> Optional[Project]:
        """
        Запрашивает у трекера проект по имени
        :param project_name: name запрашиваемого проекта
        :return: возвращает Project или None
        """
        return None

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Запрашивает у трекера задачу по id, если задачи поддерживаются трекером
        :param task_id: id запрашиваемой задачи
        :return: возвращает Task или None
        """
        return None

    def list_tasks_in_project(self, project_id: int, all: bool = False) -> Optional[List[Task]]:
        """
        Запрашивает у трекера список задач по id проекта, если задачи поддерживаются трекером
        :param project_id: id проекта
        :param all: возвращать все задачи. По-умолчанию возвращает только открытые
        :return: возвращает список задач или None
        """
        return None

    def list_activities_in_date(self, date: dt.date) -> Optional[List[Activity]]:
        """
        Запрашивает у трекера список активностей по дате
        :param date: дата
        :return: возвращает список активностей или None
        """
        return None

    def list_activities_in_date_interval(self, date_start: dt.date, date_end: dt.date) -> Optional[List[Activity]]:
        """
        Запрашивает у трекера список активностей в интервале дат
        :param date_start: начальная дата
        :param date_end: конечная дата
        :return: возвращает список активностей или None
        """
        return None

    def list_activities_in_task(self, task_id: int) -> Optional[List[Activity]]:
        """
        Запрашивает у трекера список активностей по id задачи, если задачи поддерживаются трекером
        :param task_id: id задачи
        :return: возвращает список активностей или None
        """
        return None

    def list_activities_in_project(self, project_id: int) -> Optional[List[Activity]]:
        """
        Запрашивает у трекера список активностей по id проекта
        :param project_id: id проекта
        :return: возвращает список активностей или None
        """
        return None

    def new_activity(self, activity: Activity) -> Optional[int]:
        """
        Создает новую активность на трекере
        :param activity: активность
        :return: возвращает activity_id созданной активности, или None, в случае неудачи
        """
        return None
