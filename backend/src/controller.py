from backend.src.hamster import Fact
from flask import jsonify
from functools import wraps


class Response(object):
    def __init__(self):
        self.status = True

    def send(self):
        return jsonify(self.__dict__)


class ApiController:
    def __init__(self):
        # сюда складывать данные для json-ответа. Допустимый формат - все, что поддается сериализации в json
        # для объектов это obj.__dict__
        self.response = Response()

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
        if fact.validate() is False:
            self.response.status = False
        else:
            self.response.fact = fact.__dict__
