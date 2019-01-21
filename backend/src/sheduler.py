from backend.src.model.mysql import db, User, TrackerUserLink, Project, TrackerProjectLink, Task
import requests
from .model.tracker import Tracker, Activity as TrackerActivity
from .export import Export


class Sheduler:
    user = ...  # type: User

    def __init__(self, user=None):
        if user is not None:
            self.user = user
            self.tracker_links = db.session.query(TrackerUserLink).filter(TrackerUserLink.user_id == self.user.id).all()

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

            api = Tracker.get_api(link.tracker.type, link.tracker.api_url, link.external_api_key)
            auth = self.__check_auth(link.tracker.type, link.tracker.api_url, api)
            if not auth:
                continue
            projects = api.get_all_projects()

            titles = {pr['name'].lower() for pr in projects}

            db_projects = db.session.query(Project).filter(Project.title.in_(titles)).all()
            exist = {db_pr.title for db_pr in db_projects}
            new = titles - exist
            for project in projects:
                if project['identifier'].lower() in new:
                    db_project = Project(code=project['identifier'].lower(), title=project['name'].lower())
                    project_link = TrackerProjectLink(external_project_title=project['name'].lower(),
                                                      external_project_id=project['id'],
                                                      tracker=link.tracker,
                                                      project=db_project)
                    db.session.add(project_link)
                else:
                    # найти проект по имени, проверить, стоит ли у него привязка к текущему трекеру,
                    # если не стоит - добавляем связь.
                    # Т.о. у одноименных в редмайне и эво проектов сразу будет соответствие в обоих трекерах
                    db_project = db.session.query(Project).filter(Project.title == project['name'].lower()).first()
                    if db_project is not None:
                        tracker_link = db.session.query(TrackerProjectLink) \
                            .filter(TrackerProjectLink.tracker_id == link.tracker.id) \
                            .filter(TrackerProjectLink.project_id == db_project.id) \
                            .first()
                        if tracker_link is None:
                            project_link = TrackerProjectLink(external_project_title=project['name'].lower(),
                                                              external_project_id=project['id'],
                                                              tracker=link.tracker,
                                                              project=db_project)
                            db.session.add(project_link)

        db.session.commit()

    def __fetch_evo_projects(self):
        for link in self.tracker_links:  # type: TrackerUserLink
            if link.tracker.type != 'evo':
                continue

            api = Tracker.get_api(link.tracker.type, link.tracker.api_url, link.external_api_key)
            auth = api.is_auth()
            if not auth:
                continue
            projects = api.get_all_projects()

            codes = {pr['identifier'].lower() for pr in projects}
            db_projects = db.session.query(Project).filter(Project.code.in_(codes)).all()
            exist = {db_pr.code for db_pr in db_projects}
            new = codes - exist
            for project in projects:
                if project['identifier'].lower() in new:
                    db_project = Project(code=project['identifier'].lower(), title=project['name'].lower())
                    project_link = TrackerProjectLink(external_project_title=project['name'].lower(),
                                                      external_project_id=project['id'],
                                                      tracker=link.tracker,
                                                      project=db_project)
                    db.session.add(project_link)

        db.session.commit()

    def __fetch_tasks(self):
        for link in self.tracker_links:  # type: TrackerUserLink
            if link.tracker.type != 'redmine':
                continue
            api = Tracker.get_api(link.tracker.type, link.tracker.api_url, link.external_api_key)
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
        api = Tracker.get_api(type, url, login=login, password=password)
        if api.is_auth():
            return api.get_api_key()

    def get_evo_users(self, url, token, name=False):
        api = Tracker.get_api('evo', url, api_key=token)
        if api.is_auth():
            return api.get_employers(name)

    def get_projects(self, type, url, token):
        api = Tracker.get_api(type, url, api_key=token)
        if api.is_auth():
            projects = api.get_all_projects()

            result = []
            for project in projects:
                result.append({
                    'label': project['name'],
                    'value': project['id']
                })

            return result

    def get_task(self, type, url, token, task_id):
        api = Tracker.get_api(type, url, api_key=token)
        if api.is_auth():
            external_task = api.get_task_by_id(task_id)
            if external_task is None:
                return None

            # print(external_task.__dict__)
            result = {
                'id': external_task.id,
                'tracker': external_task.tracker_name,
                'project': external_task.project_name,
                'project_id': external_task.project_id,
                'status': external_task.status,
                'name': external_task.name
            }

            return result

    def export(self, link: TrackerUserLink, export_task: TrackerActivity):
        api = Tracker.get_api(link.tracker.type, link.tracker.api_url, api_key=link.external_api_key)
        if api.is_auth():
            export_task.project_id=25
            import datetime as dt
            export_task.date=dt.date.today()-dt.timedelta(days=3)
            export = Export(export_task, link)
            if export.init() is True:
                result = export.get_status()
            # result = api.new_activity(export_task)

            return result
