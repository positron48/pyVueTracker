from backend.src.model.hamster import Fact, FormattedFact
from backend.src.model.mysql import Activity
from backend.src.engine import Engine
from flask import jsonify
from functools import wraps
from backend.src.sheduler import Sheduler


class Response(object):
    def __init__(self):
        self.status = True
        self.message = None

    def send(self):
        return jsonify(self.__dict__)


# noinspection PyArgumentList
class ApiController(object):
    def __init__(self):
        # сюда складывать данные для json-ответа. Допустимый формат - все, что поддается сериализации в json
        # для объектов это obj.__dict__
        self.response = Response()
        self.engine = Engine()

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
                task['task_id'] = task['activity_id']
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
        result = []
        for db_fact in self.engine.get_facts(dateFrom, dateTo):
            fact = FormattedFact(db_fact)
            task = {
                'id': fact.id,
                'start': fact.start_time,
                # 'end': fact.end_time,
                'hours': fact.delta,
                'description': fact.description or '',
                'name': fact.activity,
                'cat': fact.category,
                'tag': fact.tags
            }
            result.append(task)
        self.response.status = len(result) > 0
        self.response.tasks = result

    @send_response
    def get_token(self, tracker_id, login, password):
        tracker = self.engine.get_tracker(tracker_id)
        s = Sheduler()

        token = s.get_token(tracker.type, tracker.api_url, login, password)
        print(token)

        self.response.status = token is not None

        if self.response.status:
            self.response.external_token = token

            #редактируем связь пользователя с токеном, добавляя апи ключ
            self.engine.set_api_key(tracker_id, token)

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
                'external_user_id': tracker[1].external_user_id,
            }
            result.append(element)

        self.response.status = len(result) > 0
        self.response.trackers = result
