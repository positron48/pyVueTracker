from typing import Union, Sequence, List, Optional
import datetime as dt


class User:
    def __init__(self, id: int):
        self.id = id


class Project:
    def __init__(self, id: int, code: Optional[str], name: Optional[str]):
        self.id = id
        self.code = code
        self.name = name


class Task:
    def __init__(self, id: int, name: str, project: Project):
        self.id = id
        self.name = name
        self.project = project


class Activity:
    def __init__(self, id: int, user: User, date: dt.date, time: float, task: Optional[Task], comment: Optional[str],
                 title: Optional[str]):
        self.id = id
        self.user = user
        self.date = date
        self.time = time
        self.task = task
        self.comment = comment
        self.title = title


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

    def get_task_by_name(self, task_name: str) -> Optional[Task]:
        """
        Запрашивает у трекера задачу по имени, если задачи поддерживаются трекером
        :param task_name: name запрашиваемой задачи
        :return: возвращает Task или None
        """
        return None

    def list_tasks_in_project(self, project_id: int) -> Optional[List[Task]]:
        """
        Запрашивает у трекера список задач по id проекта, если задачи поддерживаются трекером
        :param project_id: id проекта
        :return: возвращает список задач или None
        """
        return None

    def get_activity_by_id(self, activity_id: int) -> Optional[Activity]:
        """
        Запрашивает у трекера активность по id
        :param activity_id: id запрошиваемой активности
        :return: возвращает Activity или None
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

    def update_activity(self, activity: Activity) -> bool:
        """
        Обновляет активность на трекере, если это поддерживается трекером
        :param activity: активность
        :return: возвращает True, или False, в случае неудачи
        """
        return False
