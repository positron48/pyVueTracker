from ..tracker import *
from typing import Union, Sequence, List, Optional, Any
import requests
import datetime as dt
import dateutil.relativedelta as dtr
import sys
import json


class Evolution(Tracker):

    def __init__(self, url, token=False, login=None, password=None):
        self.url = url
        self.token = token
        self.login = login
        self.password = password
        self.auth = None

        if token is None:
            if login is None or password is None:
                raise AttributeError
            else:
                self.token = self.get_token(login, password)
        self.auth = self.is_auth()

    def __get_project_by_key_value(self, key: str, value) -> Optional[Project]:
        if self.auth:
            projects = self.get_all_projects()
            for item in projects:
                if item[key] == value:
                    return Project(id=item['id'], code=item['identifier'], name=item['title'])

    def __get_activities_by_filter(self, project_id: int = None, user_id: int = None, start: int = None,
                                   date_start: dt.date = None, date_end: dt.date = None, limit: int = None,
                                   only_count: bool = False):
        if not self.auth:
            return None
        params = {'token': self.token,
                  'filter[date][from]': date_start,
                  'filter[date][to]': date_end,
                  'limit': limit,
                  'start': start,
                  'filter[employer_id]': user_id,
                  'filter[project_id]': project_id
                  }
        if only_count:
            params['limit'] = 1

        response = requests.get(self.url + "/api/task", params)
        response = response.json()
        if only_count:
            return int(response.get('totalCount', 0))
        if 'data' not in response or len(response['data']) < 1:
            return None
        result = []
        for item in response['data']:
            comment = item.get('comment') or ''
            if comment == '':
                comment = None
            result.append(
                Activity(
                    id=int(item.get('id')),
                    task_id=int(item.get('task_id')),
                    user_id=int(item.get('employer_id')),
                    date=dt.datetime.strptime(item.get('date'), "%d.%m.%Y").date(),
                    time=float(item.get('time')),
                    comment=comment,
                    title=item.get('title'),
                    project_id=int(item.get('project_id'))
                ))
        return result

    ######################################### Tracker interface ########################################################

    def get_tracker_type(self) -> Optional[str]:
        """
        Возвращает тип трекера
        """
        return 'evo'

    def is_auth(self) -> bool:
        """
        Проверяет, авторизован ли пользователь на трекере
        """
        if self.auth is None:
            self.auth = False
            if self.get_employers():
                self.auth = True
        return self.auth

    def get_api_key(self) -> Optional[str]:
        """
        Получает api_key пользователя для трекера, если трекер имеет такую возможность
        :return: возвращает api_key или None
        """
        return self.token

    def list_projects(self) -> Optional[List[Project]]:
        """
        Запрашивает список проектов у трекера
        :return: возвращает список проектов или None
        """
        if self.auth:
            projects = self.get_all_projects()
            return [Project(id=item['id'], code=item['identifier'], name=item['title']) for item in projects]

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        """
        Запрашивает у трекера проект по id
        :param project_id: id запрашиваемого проекта
        :return: возвращает Project или None
        """
        return self.__get_project_by_key_value('id', project_id)

    def get_project_by_code(self, project_code: str) -> Optional[Project]:
        """
        Запрашивает у трекера проект по коду
        :param project_code: code запрашиваемого проекта
        :return: возвращает Project или None
        """
        return self.__get_project_by_key_value('identifier', project_code)

    def get_project_by_name(self, project_name: str) -> Optional[Project]:
        """
        Запрашивает у трекера проект по имени
        :param project_name: name запрашиваемого проекта
        :return: возвращает Project или None
        """
        return self.__get_project_by_key_value('title', project_name)

    def list_activities_in_date(self, date: dt.date, user_id: int = None, **kwargs) -> Optional[List[Activity]]:
        """
        Запрашивает у трекера список активностей по дате
        :param user_id:
        :param date: дата
        :return: возвращает список активностей или None
        """
        return self.list_activities_in_date_interval(date, date, user_id, **kwargs)

    def list_activities_in_date_interval(self, date_start: dt.date, date_end: dt.date, user_id: int = None, **kwargs) -> \
    Optional[
        List[Activity]]:
        """
        Запрашивает у трекера список активностей в интервале дат
        :param user_id:
        :param date_start: начальная дата
        :param date_end: конечная дата
        :return: возвращает список активностей или None
        """
        return self.__get_activities_by_filter(date_start=date_start, date_end=date_end, user_id=user_id, **kwargs)

    def list_activities_in_project(self, project_id: int, **kwargs) -> Optional[
        List[Activity]]:
        """
        Запрашивает у трекера список активностей по id проекта
        :param project_id: id проекта
        :return: возвращает список активностей или None
        """
        return self.__get_activities_by_filter(project_id=project_id, **kwargs)

    def new_activity(self, activity: Activity) -> Optional[int]:
        """
        Создает новую активность на трекере
        :param activity: активность
        :return: возвращает activity_id созданной активности, или None, в случае неудачи
        """
        task_id = ''
        if activity.task_id > 0:
            task_id = activity.task_id

        data = {
            'token': self.token,
            'name': activity.title,
            'hours': activity.time,
            'date': activity.date.strftime('%d.%m.%Y'),
            'comment': activity.comment,
            'employee_id': activity.user_id,
            'project_id': activity.project_id,
            'task_id': activity.task_id
        }
        response = requests.post(self.url + "/api/task", data=data)
        response = response.json()
        if "success" in response and response['success']:
            return response['id']

    ######################################### end Tracker interface ####################################################

    def get_token(self, user, password):
        response = requests.post(self.url + "/api/auth", {"username": user, "password": password})
        response = response.json()
        if "success" in response and response['success']:
            return response['token']

    def get_employers(self, name=False):
        params = {"token": self.token}
        if name:
            params['title_start'] = name

        response = requests.get(self.url + "/api/employee", params)
        response = response.json()

        if "data" in response and len(response['data']) > 0:
            return response['data']
        else:
            return False

    def get_employeer_id(self, name=False):
        employeers = self.get_employers(name)
        if len(employeers) == 1:
            return employeers[0]['id']
        return False

    def get_all_projects(self, name=False):
        params = {"token": self.token}
        if name:
            params['title_start'] = name

        response = requests.get(self.url + "/api/project", params)
        response = response.json()

        if "data" in response and len(response['data']) > 0:
            for project in response['data']:
                project['name'] = project['title']
                project['identifier'] = project['title']

            return response['data']
        else:
            return False

    def send_task(self, name, date, hours, comment, employer_id, project_id):
        if len(date) == 8:
            date = dt.datetime.strptime(date, "%d.%m.%y").date().strftime('%d.%m.%Y')

        params = {
            "token": self.token,
            "name": name,
            "date": date,
            "hours": hours,
            "comment": comment,
            "employee_id": employer_id,
            "project_id": project_id
        }

        response = requests.post(self.url + "/api/task", params)

        response = response.json()

        if "success" in response and response['id'] > 0:
            return response['id']
        else:
            return response['id']
