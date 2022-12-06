from ..tracker import *
from typing import Union, Sequence, List, Optional, Any
import datetime as dt
import requests
from requests.auth import HTTPBasicAuth
import re


class Jira(Tracker):
    def __init__(self, url, token=None, login=None, password=None):

        if token is not None:
            print(token, flush=True)
            print(re.split(':', token), flush=True)

            data = re.split(':', token)
            login = data[0]
            password = data[1]

        if login is None or password is None:
            raise AttributeError

        self.url = url
        self.login = login
        self.password = password
        self.auth = None

        self.auth = self.is_auth()


    ######################################### Tracker interface ########################################################
    def get_tracker_type(self) -> Optional[str]:
        """
        Возвращает тип трекера
        """
        return 'jira'

    def is_auth(self) -> bool:
        """
        Проверяет, авторизован ли пользователь на трекере
        """
        if self.auth is None:
            self.auth = False
            if self.get_user_key():
                self.auth = True
        return self.auth

    def get_api_key(self) -> Optional[str]:
        """
        Получает api_key пользователя для трекера, если трекер имеет такую возможность
        :return: возвращает api_key или None
        """
        return self.login + ':' + self.password

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

    def list_activities_in_date(self, date: dt.date, user_id: int = None, **kwargs) -> Optional[List[Activity]]:
        """
        Запрашивает у трекера список активностей по дате
        :param user_id:
        :param date: дата
        :return: возвращает список активностей или None
        """
        return None

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
        return None

    def list_activities_in_project(self, project_id: int, **kwargs) -> Optional[
        List[Activity]]:
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
        data = {
            "billableSeconds": activity.time * 3600,
            "comment": activity.comment,
            "endDate": activity.date.strftime('%Y-%m-%d'),
            "includeNonWorkingDays": false,
            "originTaskId": activity.task_id,
            "started": activity.date.strftime('%Y-%m-%d'),
            "timeSpentSeconds": activity.time * 3600,
            "worker": activity.user_id
        }

        basic = HTTPBasicAuth(self.login, self.password)

        response = requests.post(self.url + "/rest/tempo-timesheets/4/worklogs", auth=(self.login, self.password), data=data)
        response = response.json()
        if "errors" in response and len(response['reasons']) > 0:
            return response['reasons'][0]
        elif len(response) > 0:
            return response[0]['tempoWorklogId']

    ######################################### end Tracker interface ####################################################
    def get_all_projects(self, name=False):
        return []

    def get_user_key(self):

        response = requests.get(self.url + "/rest/api/2/user?username=" + self.login, auth=(self.login, self.password))

        print(response.status_code, flush=True)

        if response.status_code > 400:
            return False

        print(response, flush=True)

        response = response.json()

        print(response, flush=True)

        if "errors" in response and len(response['reasons']) > 0:
            return False
        elif 'key' in response:
            print(response['key'], flush=True)
            return response['key']