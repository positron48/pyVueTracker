import requests
import datetime
import sys
import json

class Evolution:

    def __init__(self, url, token=False, login=None, password=None):
        self.url = url
        self.token = token
        self.login = login
        self.password = password

        if token is None and login is not None and password is not None:
            self.get_token(login, password)

    def is_auth(self):
        if self.get_employers():
            return True
        return False

    def get_token(self, user, password):
        response = requests.post(self.url + "/api/auth", {"username":user, "password":password})
        response = response.json()

        if "success" in response and response['success']:
            self.token = response['token']
            return self.token
        else:
            return False

    def get_api_key(self):
        return self.token

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
            date = datetime.datetime.strptime(date, "%d.%m.%y").date().strftime('%d.%m.%Y')

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