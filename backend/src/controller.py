from backend.src.model.hamster import Fact
from backend.src.engine import Engine
from flask import jsonify
from functools import wraps


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
        self.response.status = fact.validate()
        if self.response.status:
            self.response.status, self.response.message = self.engine.add_fact(fact)
        if not self.response.status and self.response.message is None:
            self.response.message = 'Не заполнена обязательная часть:\n' \
                                    'время номер_задачи [имя_активности][@проект] [#тег], [#тег2], [описание]'

    @send_response
    def get_autocomlete(self, text):
        self.response.values = self.engine.get_autocomplete(text)
        self.response.status = self.response.values is not None

    @send_response
    def get_current(self):
        current = self.engine.get_current()
        self.response.status = current is not None
        if self.response.status:
            for k, v in current.__dict__.items():
                self.response.__dict__[k] = v

    @send_response
    def get_tasks(self, dateFrom, dateTo):
        facts = self.engine.get_facts(dateFrom, dateTo)
        self.response.tasks = []
        self.response.status = facts is not None
        if self.response.status:
            for fact in facts:
                self.response.tasks.append(fact.__dict__)

    @send_response
    def delete_task(self, id):
        self.response.status = self.engine.delete_fact(id)

    @send_response
    def stop_task(self, id):
        self.response.status = self.engine.stop_fact(id)

    @send_response
    def resume_task(self, id):
        self.response.status = self.engine.resume_fact(id)
