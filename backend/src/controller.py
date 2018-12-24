from backend.src.hamster import Fact
from backend.src.logic import Logic
from flask import jsonify
from functools import wraps


class Response(object):
    def __init__(self):
        self.status = True
        self.message = None

    def send(self):
        return jsonify(self.__dict__)


class ApiController(object):
    def __init__(self):
        # сюда складывать данные для json-ответа. Допустимый формат - все, что поддается сериализации в json
        # для объектов это obj.__dict__
        self.response = Response()
        self.logic = Logic()

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
            self.response.status, self.response.message = self.logic.add_fact(fact)
        if self.response.status is False and self.response.message is None:
            self.response.message = 'Не заполнена обязательная часть:\nвремя номер_задачи [имя_активности][@проект] [#тег], [#тег2], [описание]'
        if self.response.status is True:
            del self.response.message
