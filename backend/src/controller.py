from backend.src.model.hamster import Fact, FormattedFact
from backend.src.model.mysql import Activity
from backend.src.engine import Engine
from backend.src.auth import Auth
from flask import jsonify
from functools import wraps
from backend.src.sheduler import Sheduler
from math import ceil
import copy


class Response:
    def __init__(self):
        self.status = True
        self.message = None

    def send(self):
        return jsonify(self.__dict__)


# noinspection PyArgumentList
class ApiController:
    def __init__(self):
        # сюда складывать данные для json-ответа. Допустимый формат - все, что поддается сериализации в json
        # для объектов это obj.__dict__
        self.response = Response()
        self.engine = Engine()
        self.user = Auth.get_request_user()

    # декоратор, возвращающий self.response, сериализованный в json, после отработки декорированной функции
    # декорированные функции во время работы должны изменить self.response
    def send_response(func):
        @wraps(func)
        def argument_router(self, *args, **kwargs):
            func(self, *args, **kwargs)
            return self.response.send()

        return argument_router

    @send_response
    def add_activity(self, text):
        fact = Fact(text)
        self.response.fact = fact.__dict__
        result = self.engine.add_fact(fact)
        self.response.status = isinstance(result, bool)
        if isinstance(result, str):
            self.response.message = result

    @send_response
    def get_autocomlete(self, text):
        result = []
        for db_fact in self.engine.get_autocomplete(text):  # type: Activity
            result.append(Fact(db_fact).as_text())
        self.response.values = result
        self.response.status = len(self.response.values) > 0

    @send_response
    def get_current(self):
        current = self.engine.get_current()
        self.response.status = current is not None
        if self.response.status:
            for k, v in FormattedFact(current).__dict__.items():
                self.response.__dict__[k] = v

    @send_response
    def get_tasks(self, dateFrom, dateTo):
        facts = self.engine.get_facts(dateFrom, dateTo)
        self.response.status = facts is not None
        self.response.tasks = []
        if self.response.status:
            for fact in facts:
                task = FormattedFact(fact).__dict__
                self.response.tasks.append(task)

    @send_response
    def delete_task(self, id):
        self.response.status = self.engine.delete_fact(id)

    @send_response
    def stop_task(self, id):
        self.response.status = self.engine.stop_fact(id)

    @send_response
    def resume_task(self, id):
        self.response.status = self.engine.resume_fact(id)

    @send_response
    def edit_task(self, id, fact):
        self.response.fact = fact.__dict__
        result = self.engine.edit_fact(id, fact)
        self.response.status = isinstance(result, bool)
        if isinstance(result, str):
            self.response.message = result

    @send_response
    def get_grouped_tasks(self, dateFrom, dateTo):
        tasks = []
        for db_fact in self.engine.get_facts(dateFrom, dateTo):  # type: Activity
            if db_fact.time_end is None:  # не учитываем открытые активности
                continue
            fact = FormattedFact(db_fact)
            task = {
                'id': fact.id,
                'date': fact.date,
                # 'end': fact.end_time,
                'hours': fact.delta,
                'description': fact.description or '',
                'name': fact.activity,
                'cat': fact.category,
                'tag': fact.tags,
                'task_id': fact.task_id,
                'project_id': db_fact.task.project.id
            }
            tasks.append(task)

        # format data: group by date, task_id
        formated_tasks = {}
        for task in tasks:
            taskDate = task['date']
            if not taskDate in formated_tasks:
                formated_tasks[taskDate] = {}
            if task['task_id'] == '' or task['task_id'] is None:
                task['task_id'] = 'empty_' + task['cat']

            if not task['task_id'] in formated_tasks[taskDate]:
                formated_tasks[taskDate][task['task_id']] = copy.copy(task)
                formated_tasks[taskDate][task['task_id']]['description'] = []
            else:
                formated_tasks[taskDate][task['task_id']]['hours'] += task['hours']

            description = copy.copy(task['description'])
            if description is not '':
                formated_tasks[taskDate][task['task_id']]['description'].append(description)
        print(formated_tasks)

        tasks = []
        i = 0
        for formated_tasks in formated_tasks.values():
            for task in formated_tasks.values():
                description = ', '.join(list(set(task['description'])))
                if task['task_id'] is not None:
                    try:
                        task_id = int(task['task_id'])
                    except ValueError:
                        task_id = ""
                else:
                    task_id = ""

                new_task = {
                    'id': task['id'],
                    'date': task['date'],
                    'delta': ceil(task['hours'] * 10) / 10,
                    'description': description,
                    'name': task['name'],
                    'category': task['cat'],
                    'tag': task['tag'],
                    'task_id': task_id,
                    'project_id': task['project_id']
                }
                i += 1
                tasks.append(new_task)

        self.response.status = True
        self.response.tasks = tasks

    @send_response
    def get_token(self, tracker_id, login, password):
        tracker = self.engine.get_tracker(tracker_id)
        s = Sheduler()

        token = s.get_token(tracker['type'], tracker['api_url'], login, password)

        self.response.status = token is not None

        if self.response.status:
            self.response.external_token = token

            # редактируем связь пользователя с токеном, добавляя апи ключ
            self.engine.set_api_key(tracker_id, token)

    @send_response
    def get_evo_users(self):
        tracker = self.engine.get_evo_tracker()
        s = Sheduler()

        users = s.get_evo_users(tracker[0].api_url, tracker[1].external_api_key)

        evo_users = []
        if users is None:
            self.response.status = False
        else:
            for user in users:
                evo_users.append({
                    'label': user['title'],
                    'value': user['id']
                })

        self.response.users = evo_users

    @send_response
    def get_trackers(self):
        result = []
        for tracker in self.engine.get_trackers():
            element = {
                'id': tracker[0].id,
                'title': tracker[0].title,
                'type': tracker[0].type,
                'api_url': tracker[0].api_url,
                'external_api_key': tracker[1].external_api_key,
                'external_user_id': tracker[1].external_user_id
            }
            result.append(element)

        self.response.status = len(result) > 0
        self.response.trackers = result

    @send_response
    def get_projects(self, project_ids=None):
        result = {}

        user_trackers = self.engine.get_trackers()
        tracker_ids = {tracker[0].id for tracker in user_trackers}

        for project in self.engine.get_projects(project_ids):
            element = {
                'id': project.id,
                'title': project.title,
                'code': project.code,
                'tracker_projects': {}
            }

            for tracker_prop in project.tracker_properties:
                # сопоставления по приоритету - сначала привязанные к текущему пользователю,
                # затем не привязанные ни к кому
                if tracker_prop.tracker_id in tracker_ids and tracker_prop.external_project_id > 0:
                    element['tracker_projects'][tracker_prop.tracker_id] = {
                        'tracker_id': tracker_prop.tracker_id,
                        'external_project_id': tracker_prop.external_project_id,
                        'external_project_title': tracker_prop.external_project_title
                    }

            result[project.id] = element

        self.response.status = len(result) > 0
        self.response.projects = result

    @send_response
    def get_tracker_projects(self, tracker_id):
        tracker = self.engine.get_tracker(tracker_id)
        s = Sheduler()
        projects = s.get_projects(tracker['type'], tracker['api_url'], tracker['external_api_key'])

        self.response.status = len(projects) > 0
        self.response.projects = projects

    @send_response
    def save_tracker(self, id, type, title, api_url):
        result = []

        self.response.status = self.engine.save_tracker(id, type, title, api_url)
        self.response.trackers = result

    @send_response
    def save_evo_user(self, user_id):
        tracker = self.engine.get_evo_tracker()
        self.response.status = True
        self.engine.save_user_id(tracker[0].id, user_id)

    @send_response
    def delete_tracker(self, id):
        result = []

        self.response.status = self.engine.delete_tracker(id)
        self.response.trackers = result

    @send_response
    def link_project(self, project_id, tracker_id, tracker_project_id, tracker_project_title):
        result = []

        self.response.status = self.engine.link_project(project_id, tracker_id, tracker_project_id, tracker_project_title)
        self.response.trackers = result
