from backend.src.model.mysql import db, User, TrackerUserLink, Tracker, Project, TrackerProjectLink, UserProjectLink, \
    Task
from backend.src.model.redmine import Redmine
from backend.src.model.evolution import Evolution
from backend.src.auth import Auth
import requests


class Sheduler(object):
    user = ...  # type: User

    def __init__(self, user=None):
        if user is not None:
            self.user = user
            self.tracker_links = db.session.query(TrackerUserLink).filter(TrackerUserLink.user_id == self.user.id).all()

    @staticmethod
    def __get_engine(type, url, api_key=None, login=None, password=None):
        if type == 'redmine':
            return Redmine(url, api_key, login, password)
        elif type == 'evo':
            return Evolution(url, api_key, login, password)

        return None

    def __check_auth(self, type, url, api):
        response = requests.options(url)
        if response.status_code != requests.codes.ok:
            response = requests.get(url)
        if response.status_code != requests.codes.ok:
            return None
        return {
            'redmine': api.is_auth(),
            'evo': api.is_auth(),
        }[type]

    def __fetch_redmine_projects(self):
        for link in self.tracker_links:  # type: TrackerUserLink
            if link.tracker.type != 'redmine':
                continue

            api = self.__get_engine(link.tracker.type, link.tracker.api_url, link.external_api_key)
            auth = self.__check_auth(link.tracker.type, link.tracker.api_url, api)
            if not auth:
                continue
            projects = api.get_all_projects()

            codes = {pr['identifier'] for pr in projects}
            db_projects = db.session.query(Project).filter(Project.code.in_(codes)).all()
            exist = {db_pr.code for db_pr in db_projects}
            new = codes - exist
            for project in projects:
                if project['identifier'] in new:
                    db_project = Project(code=project['identifier'], title=project['name'])
                    project_link = TrackerProjectLink(external_project_title=project['name'],
                                                      external_project_id=project['id'],
                                                      tracker=link.tracker,
                                                      project=db_project)
                    user_link = UserProjectLink(project=db_project, user=self.user)
                    db.session.add(project_link)
                    db.session.add(user_link)
        db.session.commit()

    def __fetch_evo_projects(self):
        for link in self.tracker_links:  # type: TrackerUserLink
            if link.tracker.type != 'evo':
                continue

            api = self.__get_engine(link.tracker.type, link.tracker.api_url, link.external_api_key)
            auth = api.is_auth()
            if not auth:
                continue
            projects = api.get_all_projects()

            codes = {pr['id'] for pr in projects}
            db_projects = db.session.query(Project).filter(Project.code.in_(codes)).all()
            exist = {db_pr.code for db_pr in db_projects}
            new = codes - exist
            for project in projects:
                if project['id'] in new:
                    db_project = Project(code=project['id'], title=project['name'])
                    project_link = TrackerProjectLink(external_project_title=project['name'],
                                                      external_project_id=project['id'],
                                                      tracker=link.tracker,
                                                      project=db_project)
                    db.session.add(project_link)
        db.session.commit()

    def __fetch_tasks(self):
        for link in self.tracker_links:  # type: TrackerUserLink
            if link.tracker.type != 'redmine':
                continue
            api = self.__get_engine(link.tracker.type, link.tracker.api_url, link.external_api_key)
            auth = self.__check_auth(link.tracker.type, link.tracker.api_url, api)
            if not auth:
                continue
            tasks = {
                'redmine': api.get_all_tasks(),
            }[link.tracker.type]

            task_ids = {task.id for task in tasks}
            db_tasks = db.session.query(Task).filter(Task.external_task_id.in_(task_ids))
            exist_ids = {task.external_task_id for task in db_tasks}

            project_ids = {task.project['id'] for task in tasks}
            db_projects = db.session.query(TrackerProjectLink).filter(
                TrackerProjectLink.external_project_id.in_(project_ids))
            project_ids = {pr_link.external_project_id: pr_link.project_id for pr_link in db_projects}

            new_ids = task_ids - exist_ids
            new = {task.id: task for task in tasks if task.id in new_ids}
            for task_id in sorted(list(new_ids)):
                task = new[task_id]
                db_task = Task(project_id=project_ids[task.project['id']], title=task.subject, external_task_id=task.id)
                db.session.add(db_task)
        db.session.commit()

    def fetch_external_data(self):
        self.__fetch_evo_projects()
        self.__fetch_redmine_projects()
        # self.__fetch_tasks()
        return 'done!'

    def get_token(self, type, url, login, password):
        api = self.__get_engine(type, url, login=login, password=password)
        if api.is_auth():
            return api.get_api_key()

    def get_evo_users(self, url, token, name=False):
        api = self.__get_engine('evo', url, api_key=token)
        if api.is_auth():
            return api.get_employers(name)

    def get_projects(self, type, url, token):
        api = self.__get_engine(type, url, api_key=token)
        if api.is_auth():
            return api.get_all_projects()
