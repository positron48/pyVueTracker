from backend.src.model.mysql import db, User, TrackerUserLink, Tracker, Project, TrackerProjectLink, UserProjectLink, \
    Task
from backend.src.model.redmine import Redmine
from backend.src.auth import Auth
import requests


class Sheduler(object):
    user = ...  # type: User

    def __init__(self, user):
        self.user = user
        self.tracker_links = db.session.query(TrackerUserLink).filter(TrackerUserLink.user_id == self.user.id).all()

    def __get_engine(self, type, url, api_key):
        return {
            'redmine': Redmine(url, api_key),
        }[type]

    def __check_auth(self, type, url, api):
        response = requests.get(url)
        if response.status_code != requests.codes.ok:
            return None
        return {
            'redmine': api.is_auth(),
        }[type]

    def __fetch_projects(self):
        for link in self.tracker_links:  # type: TrackerUserLink
            if link.tracker.type != 'redmine':
                continue
            api = self.__get_engine(link.tracker.type, link.tracker.api_url, link.external_api_key)
            auth = self.__check_auth(link.tracker.type, link.tracker.api_url, api)
            if not auth:
                continue
            projects = {
                'redmine': api.get_all_projects(),
            }[link.tracker.type]
            codes = {pr.identifier for pr in projects}
            db_projects = db.session.query(Project).filter(Project.code.in_(codes)).all()
            exist = {db_pr.code for db_pr in db_projects}
            new = codes - exist
            for project in projects:
                if project.identifier in new:
                    db_project = Project(code=project.identifier, title=project.name)
                    project_link = TrackerProjectLink(external_project_title=project.name,
                                                      external_project_id=project.id,
                                                      tracker=link.tracker,
                                                      project=db_project)
                    user_link = UserProjectLink(project=db_project, user=self.user)
                    db.session.add(project_link)
                    db.session.add(user_link)
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
            for task in tasks:
                if task.id in new_ids:
                    db_task = Task(project_id=project_ids[task.project['id']], title=task.subject,
                                   external_task_id=task.id)
                    db.session.add(db_task)
        db.session.commit()

    def fetch_external_data(self):
        self.__fetch_projects()
        self.__fetch_tasks()
        return 'done!'
