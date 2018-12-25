from redminelib import Redmine as RedmineLib
from redminelib.exceptions import AuthError


class Redmine(object):
    def __init__(self, url, token=None, login=None,
                 password=None):
        self.api = None  # type: RedmineLib
        if token is None:
            self.api = RedmineLib(url, username=login, password=password)
        else:
            self.api = RedmineLib(url, key=token)

    def is_auth(self):
        try:
            auth = self.api.auth()
        except AuthError:
            auth = None
        return auth is not None

    def get_all_projects(self):
        return self.api.project.all()

    def get_all_tasks(self):
        return self.api.issue.all()

    def get_api_key(self):
        if self.is_auth():
            return self.api.auth().api_key
