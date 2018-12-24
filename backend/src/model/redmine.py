class Redmine(object):
    def __init__(self, url, token=None, login=None,
                 password=None):
        from redminelib import Redmine
        self.api = None  # type: Redmine
        if token is None:
            self.api = Redmine(url, username=login, password=password)
        else:
            self.api = Redmine(url, key=token)

    def get_all_projects(self):
        return self.api.project.all()

    def get_all_tasks(self):
        return self.api.issue.all()
